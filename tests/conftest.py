"""Work around genlayer-test 0.29.2's POSIX unlink on Windows.

The upstream loader installs the real SDK message on fd 0, then unlinks its
still-open temporary file. Defer only that cleanup; execution is unchanged.
"""
import os

if os.name == "nt":
    from gltest.direct import loader
    _inject = loader._inject_message_to_fd0
    _deferred = []

    def _windows_inject(vm):
        try:
            _inject(vm)
        except PermissionError as exc:
            if getattr(exc, "winerror", None) != 32 or vm._original_stdin_fd is None:
                raise
            _deferred.append(exc.filename)

    loader._inject_message_to_fd0 = _windows_inject

def pytest_sessionfinish(session, exitstatus):
    if os.name == "nt":
        for path in _deferred:
            try:
                os.unlink(path)
            except (PermissionError, FileNotFoundError):
                pass
