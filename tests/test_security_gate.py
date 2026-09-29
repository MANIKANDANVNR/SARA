from core.state import SaraState

from security.security_manager import SecurityManager

from security.security_gate import SecurityGate

from security.permission import (
    PermissionType,
    PermissionLevel
)


# =========================================================
# FACTORY
# =========================================================

def create_gate():

    state = SaraState()

    security = SecurityManager(
        state
    )

    gate = SecurityGate(
        security
    )

    return state, security, gate


# =========================================================
# TEST 1 — Gate starts denied
# =========================================================

def test_gate_denies_without_authentication():

    state, security, gate = (
        create_gate()
    )

    result = gate.check(
        PermissionType.SYSTEM,
        PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 2 — Permission must be granted
# =========================================================

def test_gate_denies_without_permission():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    result = gate.check(
        PermissionType.SYSTEM,
        PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 3 — Gate allows valid permission
# =========================================================

def test_gate_allows_valid_permission():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    result = gate.check(
        PermissionType.SYSTEM,
        PermissionLevel.LOW
    )

    assert result is True


# =========================================================
# TEST 4 — File resource required
# =========================================================

def test_gate_requires_file_resource():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    result = gate.check(
        PermissionType.READ_FILE,
        PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 5 — File resource isolation
# =========================================================

def test_gate_enforces_file_resource_isolation():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.request_permission(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="allowed.txt",
        duration=60
    )

    assert gate.check(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="allowed.txt"
    ) is True

    assert gate.check(
        PermissionType.READ_FILE,
        PermissionLevel.LOW,
        resource="other.txt"
    ) is False


# =========================================================
# TEST 6 — Request access
# =========================================================

def test_gate_can_request_access():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    result = gate.request_access(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    assert result is True

    assert security.has_permission(
        PermissionType.SYSTEM
    ) is True


# =========================================================
# TEST 7 — Request access fails when logged out
# =========================================================

def test_gate_request_access_requires_authentication():

    state, security, gate = (
        create_gate()
    )

    result = gate.request_access(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    assert result is False


# =========================================================
# TEST 8 — High-level permission still requires
# authentication and confirmation
# =========================================================

def test_gate_high_permission():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.authenticate_critical()

    security.confirmation.request_confirmation = (
        lambda message: True
    )

    result = gate.request_access(
        PermissionType.SYSTEM,
        PermissionLevel.HIGH,
        duration=60
    )

    assert result is True


# =========================================================
# TEST 9 — Tool authorization
# =========================================================

def test_tool_authorization():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    result = gate.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is True


# =========================================================
# TEST 10 — Tool authorization denied
# =========================================================

def test_tool_authorization_denied():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    result = gate.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 11 — Tool name required
# =========================================================

def test_tool_name_required():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    result = gate.authorize_tool(
        tool_name="",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 12 — Emergency shutdown blocks gate
# =========================================================

def test_emergency_shutdown_blocks_gate():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    security.emergency_shutdown()

    result = gate.check(
        PermissionType.SYSTEM,
        PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 13 — Logout blocks gate
# =========================================================

def test_logout_blocks_gate():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    security.logout()

    result = gate.check(
        PermissionType.SYSTEM,
        PermissionLevel.LOW
    )

    assert result is False


# =========================================================
# TEST 14 — Tool access request
# =========================================================

def test_request_tool_access():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    result = gate.request_tool_access(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW,
        duration=60
    )

    assert result is True


# =========================================================
# TEST 15 — Tool access request denied
# =========================================================

def test_request_tool_access_denied():

    state, security, gate = (
        create_gate()
    )

    result = gate.request_tool_access(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW,
        duration=60
    )

    assert result is False


# =========================================================
# TEST 16 — Permission expiration blocks gate
# =========================================================

def test_expired_permission_blocks_gate():

    state, security, gate = (
        create_gate()
    )

    security.authenticate()

    security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=1
    )

    import time

    time.sleep(2)

    result = gate.check(
        PermissionType.SYSTEM,
        PermissionLevel.LOW
    )

    assert result is False