import copy
import json
import pytest


OP = {"action": "publish", "resource": "community/announcements", "body": "Workshop starts Saturday. Everyone is welcome."}
CLAUSES = ["The message must announce an educational event.", "The message must not solicit money or credentials."]


def verdict(decision="ALLOW", confidence="high"):
    return {"clauses": [{"id": i, "decision": decision, "confidence": confidence} for i in range(2)]}


def mock(vm, obj):
    vm.clear_mocks()
    vm.mock_llm(r"SCOPELOCK_V1", json.dumps(obj))


@pytest.fixture
def setup(direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie):
    direct_vm.warp("2026-10-10T00:00:00Z")
    direct_vm.sender = direct_alice
    c = direct_deploy("contracts/scopelock.py", sdk_version="v0.2.12")
    from genlayer import Address
    g = c.create_grant(Address(direct_bob), Address(direct_charlie), json.dumps(CLAUSES), '["publish"]', 10, 2, 3600)
    direct_vm.sender = direct_bob
    mock(direct_vm, verdict())
    return c, g


def issue(c, g, nonce=1, units=4, op=OP):
    return c.request_permit(g, nonce, json.dumps(op), units, 300)


def test_full_reserve_consume_flow(setup, direct_vm, direct_charlie):
    c, g = setup
    p = issue(c, g)
    assert c.get_grant(g)["reserved_units"] == 4
    assert direct_vm.run_validator() is True  # explicitly execute captured validator
    direct_vm.sender = direct_charlie
    receipt = c.consume(p, json.dumps(OP, indent=2))
    assert receipt["operation"] == OP
    assert len(receipt["digest"]) == 64
    assert c.get_permit(p)["status"] == "CONSUMED"
    assert c.get_grant(g)["spent_units"] == 4
    assert c.get_grant(g)["reserved_units"] == 0
    with direct_vm.expect_revert("Permit not consumable"):
        c.consume(p, json.dumps(OP))


@pytest.mark.parametrize("confidence", ["medium", "low"])
def test_exact_confidence_is_bound(setup, direct_vm, confidence):
    c, g = setup
    issue(c, g)
    mock(direct_vm, verdict(confidence=confidence))
    assert direct_vm.run_validator() is False


@pytest.mark.parametrize("decision", ["DENY", "UNKNOWN"])
def test_each_clause_is_independently_bound(setup, direct_vm, decision):
    c, g = setup
    issue(c, g)
    obj = verdict()
    obj["clauses"][1]["decision"] = decision
    mock(direct_vm, obj)
    assert direct_vm.run_validator() is False


def test_clause_order_can_differ_without_changing_meaning(setup, direct_vm):
    c, g = setup
    issue(c, g)
    obj = verdict()
    obj["clauses"].reverse()
    mock(direct_vm, obj)
    assert direct_vm.run_validator() is True


@pytest.mark.parametrize("decision,confidence", [("ALLOW", "medium"), ("ALLOW", "low"), ("DENY", "high"), ("UNKNOWN", "high")])
def test_non_high_or_non_allow_never_reserves(setup, direct_vm, decision, confidence):
    c, g = setup
    mock(direct_vm, verdict(decision, confidence))
    p = issue(c, g)
    assert c.get_permit(p)["status"] == "REJECTED"
    assert c.get_grant(g)["reserved_units"] == 0
    assert c.get_grant(g)["reserved_uses"] == 0


def test_malformed_leader_and_error_disagree(setup, direct_vm):
    c, g = setup
    issue(c, g)
    assert direct_vm.run_validator(leader_result=[{"id": 0}]) is False
    assert direct_vm.run_validator(leader_error=RuntimeError("transient")) is False
    duplicate = verdict()["clauses"]
    duplicate[1]["id"] = 0
    assert direct_vm.run_validator(leader_result=duplicate) is False


def test_invalid_model_output_does_not_write_state(setup, direct_vm):
    c, g = setup
    before = copy.deepcopy(c.get_grant(g))
    mock(direct_vm, {"clauses": []})
    with direct_vm.expect_revert("Missing or extra clause"):
        issue(c, g)
    assert c.get_grant(g) == before
    mock(direct_vm, verdict())
    assert issue(c, g) == 1  # failed attempt did not consume nonce/id


def test_nonce_cannot_be_replayed_even_after_rejection(setup, direct_vm):
    c, g = setup
    mock(direct_vm, verdict("DENY"))
    issue(c, g)
    mock(direct_vm, verdict())
    with direct_vm.expect_revert("Nonce already used"):
        issue(c, g)


def test_payload_substitution_and_wrong_consumer(setup, direct_vm, direct_charlie):
    c, g = setup
    p = issue(c, g)
    with direct_vm.expect_revert("Only bound consumer"):
        c.consume(p, json.dumps(OP))
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("Operation does not match"):
        c.consume(p, json.dumps({**OP, "body": "Send funds now"}))
    assert c.get_permit(p)["status"] == "READY"


def test_reservations_prevent_overbooking_and_release_restores_quota(setup, direct_vm):
    c, g = setup
    p = issue(c, g, units=7)
    with direct_vm.expect_revert("Quota exhausted"):
        issue(c, g, nonce=2, units=4)
    c.release(p)
    issue(c, g, nonce=2, units=10)
    assert c.get_grant(g)["reserved_units"] == 10
    with direct_vm.expect_revert("No reservation"):
        c.release(p)


def test_revocation_invalidates_live_permit_and_anyone_can_release(setup, direct_vm, direct_alice, direct_charlie):
    c, g = setup
    p = issue(c, g)
    with direct_vm.expect_revert("Only owner"):
        c.revoke(g)
    direct_vm.sender = direct_alice
    c.revoke(g)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("Permit not consumable"):
        c.consume(p, json.dumps(OP))
    c.release(p)
    assert c.get_grant(g)["reserved_units"] == 0


def test_expiry_boundary_permissionless_cleanup(setup, direct_vm, direct_charlie):
    c, g = setup
    p = issue(c, g)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("Only owner or delegate"):
        c.release(p)
    direct_vm.warp("2026-10-10T00:05:00Z")
    with direct_vm.expect_revert("Permit not consumable"):
        c.consume(p, json.dumps(OP))
    c.release(p)
    assert c.get_grant(g)["reserved_uses"] == 0


def test_deterministic_allowlist_before_llm(setup, direct_vm):
    c, g = setup
    with direct_vm.expect_revert("Action outside allowlist"):
        issue(c, g, op={**OP, "action": "transfer"})
    with direct_vm.expect_revert("Expected action"):
        issue(c, g, op={**OP, "hidden": "transfer"})


def test_domain_commitments_differ_by_nonce_and_units(setup):
    c, g = setup
    p1 = issue(c, g, 1, 4)
    p2 = issue(c, g, 2, 5)
    assert c.get_permit(p1)["digest"] != c.get_permit(p2)["digest"]
    commitment = c.get_permit(p1)["commitment"]
    assert all(k in commitment for k in ("chain_id", "contract", "consumer", "grant_id", "nonce", "units", "operation"))


def test_use_limit_is_separate_from_unit_limit(setup, direct_vm):
    c, g = setup
    issue(c, g, 1, 1)
    issue(c, g, 2, 1)
    with direct_vm.expect_revert("Quota exhausted"):
        issue(c, g, 3, 1)


def test_only_delegate_can_request(setup, direct_vm, direct_alice):
    c, g = setup
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("Only delegate"):
        issue(c, g)


def test_permit_cannot_outlive_grant(setup, direct_vm):
    c, g = setup
    direct_vm.warp("2026-10-10T00:59:30Z")
    p = issue(c, g)
    assert c.get_permit(p)["expires_at"] == c.get_grant(g)["expires_at"]
    direct_vm.warp("2026-10-10T01:00:00Z")
    with direct_vm.expect_revert("Inactive grant"):
        issue(c, g, 2)


def test_boolean_and_extra_leader_clause_ids_are_rejected(setup, direct_vm):
    c, g = setup
    issue(c, g)
    obj = verdict()["clauses"]
    obj[0]["id"] = False
    assert direct_vm.run_validator(leader_result=obj) is False
    assert direct_vm.run_validator(leader_result=verdict()["clauses"] + [verdict()["clauses"][0]]) is False
