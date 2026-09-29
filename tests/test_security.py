import time

from security.security_gate import SecurityGate

from core.state import SaraState

from security.security_manager import SecurityManager

from security.permission import (
    PermissionType,
    PermissionLevel
)


# =========================================================
# TEST 1 — Authentication starts disabled
# =========================================================

def test_authentication_starts_disabled():

    state = SaraState()

    security = SecurityManager(state)

    assert security.is_authenticated() is False


# =========================================================
# TEST 2 — Basic authentication
# =========================================================

def test_authentication():

    state = SaraState()

    security = SecurityManager(state)

    result = security.authenticate()

    assert result is True

    assert security.is_authenticated() is True


# =========================================================
# TEST 3 — Permission denied without authentication
# =========================================================

def test_permission_denied_without_authentication():

    state = SaraState()

    security = SecurityManager(state)

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert result is False


# =========================================================
# TEST 4 — LOW permission requires BASIC
# =========================================================

def test_low_permission_requires_basic():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert result is True


# =========================================================
# TEST 5 — MEDIUM permission requires STRONG
# =========================================================

def test_medium_permission_requires_strong():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.MEDIUM,
        resource="test.txt",
        duration=60
    )

    assert result is False

    security.authenticate_strong()

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.MEDIUM,
        resource="test.txt",
        duration=60
    )

    assert result is True


# =========================================================
# TEST 6 — HIGH permission requires CRITICAL
# =========================================================

def test_high_permission_requires_critical():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.HIGH,
        resource="test.txt",
        duration=60
    )

    assert result is False

    security.authenticate_critical()

    # Bypass interactive confirmation for automated testing.
    security.confirmation.request_confirmation = (
        lambda message: True
    )

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.HIGH,
        resource="test.txt",
        duration=60
    )

    assert result is True


# =========================================================
# TEST 7 — File resource is mandatory
# =========================================================

def test_file_resource_required():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource=None,
        duration=60
    )

    assert result is False


# =========================================================
# TEST 8 — Correct resource permission
# =========================================================

def test_correct_resource_permission():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="test.txt"
    ) is True


# =========================================================
# TEST 9 — Resource isolation
# =========================================================

def test_resource_isolation():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="test.txt"
    ) is True

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="another.txt"
    ) is False


# =========================================================
# TEST 10 — Permission expiration
# =========================================================

def test_permission_expiration():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="temporary.txt",
        duration=1
    )

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="temporary.txt"
    ) is True

    time.sleep(2)

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="temporary.txt"
    ) is False


# =========================================================
# TEST 11 — Logout
# =========================================================

def test_logout():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    assert security.is_authenticated() is True

    security.logout()

    assert security.is_authenticated() is False


# =========================================================
# TEST 12 — Logout revokes permissions
# =========================================================

def test_logout_revokes_permissions():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="test.txt"
    ) is True

    security.logout()

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="test.txt"
    ) is False


# =========================================================
# TEST 13 — Emergency shutdown
# =========================================================

def test_emergency_shutdown():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    security.emergency_shutdown()

    assert state.running is False

    assert state.emergency_shutdown is True

    assert security.is_authenticated() is False

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="test.txt"
    ) is False


# =========================================================
# TEST 14 — Audit logging
# =========================================================

def test_audit_logging():

    state = SaraState()

    security = SecurityManager(state)

    security.authenticate()

    events = security.audit.get_events()

    assert len(events) > 0

    assert events[0]["event"] == "AUTHENTICATION"

def test_permission_resource_is_normalized():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    result = security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="   test.txt   ",
        duration=60
    )

    assert result is True

    assert security.has_permission(
        PermissionType.READ_FILE,
        resource="test.txt"
    ) is True

def test_permission_cannot_escalate_level():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    result = security.request_permission(
        PermissionType.CALCULATOR,
        PermissionLevel.LOW,
        duration=60
    )

    assert result is True

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is True

    # A LOW permission must not satisfy
    # a HIGH-level security requirement.
    assert security.authentication_level_sufficient(
        PermissionLevel.HIGH
    ) is False

def test_security_gate_requires_sufficient_authentication_level():

    state = SaraState()

    security = SecurityManager(
        state
    )

    gate = SecurityGate(
        security
    )

    security.authenticate()

    result = gate.request_access(
        permission_type=PermissionType.INTERNET,
        level=PermissionLevel.MEDIUM,
        duration=60
    )

    assert result is False

    assert security.has_permission(
        PermissionType.INTERNET
    ) is False

def test_file_permission_is_bound_to_specific_resource():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    result = security.request_permission(
        PermissionType.WRITE_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert result is True

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    ) is True

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="other.txt"
    ) is False

def test_expired_permission_cannot_be_used():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    result = security.request_permission(
        PermissionType.WRITE_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=0
    )

    assert result is True

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    ) is False

def test_revoked_permission_cannot_be_used():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    result = security.request_permission(
        PermissionType.WRITE_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    )

    assert result is True

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    ) is True

    security.revoke_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    )

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    ) is False

def test_revoke_all_permissions_removes_all_access():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    assert security.request_permission(
        PermissionType.CALCULATOR,
        PermissionLevel.LOW,
        duration=60
    ) is True

    assert security.request_permission(
        PermissionType.PYTHON,
        PermissionLevel.LOW,
        duration=60
    ) is True

    assert security.request_permission(
        PermissionType.WRITE_FILE,
        PermissionLevel.LOW,
        resource="test.txt",
        duration=60
    ) is True

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is True

    assert security.has_permission(
        PermissionType.PYTHON
    ) is True

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    ) is True

    security.revoke_all_permissions()

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is False

    assert security.has_permission(
        PermissionType.PYTHON
    ) is False

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource="test.txt"
    ) is False

def test_logout_invalidates_authentication_and_permissions():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    assert security.request_permission(
        PermissionType.CALCULATOR,
        PermissionLevel.LOW,
        duration=60
    ) is True

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is True

    security.logout()

    assert security.is_authenticated() is False

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is False

def test_emergency_shutdown_blocks_existing_permissions():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    assert security.request_permission(
        PermissionType.CALCULATOR,
        PermissionLevel.LOW,
        duration=60
    ) is True

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is True

    security.emergency_shutdown()

    assert state.emergency_shutdown is True

    assert state.running is False

    assert security.is_authenticated() is False

    assert security.has_permission(
        PermissionType.CALCULATOR
    ) is False

def test_security_gate_rejects_invalid_permission_type():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    gate = SecurityGate(
        security
    )

    result = gate.request_access(
        permission_type="invalid_permission",
        level=PermissionLevel.LOW
    )

    assert result is False

def test_security_gate_rejects_invalid_permission_level():

    state = SaraState()

    security = SecurityManager(
        state
    )

    security.authenticate()

    gate = SecurityGate(
        security
    )

    result = gate.request_access(
        permission_type=PermissionType.CALCULATOR,
        level="invalid_level"
    )

    assert result is False