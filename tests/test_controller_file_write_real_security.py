from pathlib import Path

from core.controller import SaraController

from core.state import (
    SaraState
)

from security.security_manager import (
    SecurityManager
)

from security.permission import (
    PermissionType,
    PermissionLevel
)

from security.security_gate import (
    SecurityGate
)

from tools.file_write_tool import (
    FileWriteTool
)


def create_controller():

    state = SaraState()

    security = SecurityManager(
        state
    )

    controller = object.__new__(
        SaraController
    )

    controller.security = security

    controller.security_gate = (
        SecurityGate(
            security
        )
    )

    controller.tools = type(
        "ToolRegistry",
        (),
        {
            "exists": lambda self, name: (
                name == "file_write"
            ),
            "get": lambda self, name: (
                FileWriteTool()
                if name == "file_write"
                else None
            )
        }
    )()

    return controller, security


def authenticate(security):
    result = security.authenticate()

    assert result is True
    assert security.is_authenticated() is True


def grant_write_permission(
    security,
    file_path
):
    result = security.request_permission(
        permission_type=(
            PermissionType.WRITE_FILE
        ),
        level=PermissionLevel.LOW,
        resource=str(file_path)
    )

    assert result is True

    assert security.has_permission(
        PermissionType.WRITE_FILE,
        resource=str(file_path)
    ) is True


def test_unauthenticated_write_is_denied(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    file_path = (
        tmp_path /
        "unauthenticated.txt"
    )

    result = controller.execute_file_write(
        str(file_path),
        "Hello SARA"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert file_path.exists() is False


def test_authenticated_without_permission_is_denied(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "no_permission.txt"
    )

    result = controller.execute_file_write(
        str(file_path),
        "Hello SARA"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert file_path.exists() is False


def test_wrong_file_resource_is_denied(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    allowed_path = (
        tmp_path /
        "allowed.txt"
    )

    blocked_path = (
        tmp_path /
        "blocked.txt"
    )

    grant_write_permission(
        security,
        allowed_path
    )

    result = controller.execute_file_write(
        str(blocked_path),
        "Should not be written"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert blocked_path.exists() is False


def test_authorized_write_creates_file(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "authorized.txt"
    )

    grant_write_permission(
        security,
        file_path
    )

    result = controller.execute_file_write(
        str(file_path),
        "Hello SARA"
    )

    assert result["success"] is True

    assert result["error"] is None

    assert file_path.exists() is True

    assert file_path.read_text(
        encoding="utf-8"
    ) == "Hello SARA"


def test_authorized_multiline_write(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "multiline.txt"
    )

    grant_write_permission(
        security,
        file_path
    )

    content = (
        "Line 1\n"
        "Line 2\n"
        "Line 3"
    )

    result = controller.execute_file_write(
        str(file_path),
        content
    )

    assert result["success"] is True

    assert file_path.read_text(
        encoding="utf-8"
    ) == content


def test_custom_encoding_write(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "utf16.txt"
    )

    grant_write_permission(
        security,
        file_path
    )

    result = controller.execute_file_write(
        str(file_path),
        "Hello SARA",
        encoding="utf-16"
    )

    assert result["success"] is True

    assert file_path.read_text(
        encoding="utf-16"
    ) == "Hello SARA"


def test_logout_removes_write_permission(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "logout.txt"
    )

    grant_write_permission(
        security,
        file_path
    )

    security.logout()

    assert security.is_authenticated() is False

    result = controller.execute_file_write(
        str(file_path),
        "Should not be written"
    )

    assert result["success"] is False

    assert file_path.exists() is False


def test_emergency_shutdown_blocks_write(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "emergency.txt"
    )

    grant_write_permission(
        security,
        file_path
    )

    security.emergency_shutdown()

    result = controller.execute_file_write(
        str(file_path),
        "Should not be written"
    )

    assert result["success"] is False

    assert file_path.exists() is False


def test_write_operation_is_audited(
    tmp_path
):
    controller, security = (
        create_controller()
    )

    authenticate(security)

    file_path = (
        tmp_path /
        "audit.txt"
    )

    grant_write_permission(
        security,
        file_path
    )

    result = controller.execute_file_write(
        str(file_path),
        "Audit test"
    )

    assert result["success"] is True

    events = security.audit.get_events()

    matching_events = [
        event
        for event in events
        if (
            event.get("event")
            == "TOOL_EXECUTION"
            and event.get("action")
            == "file_write"
        )
    ]

    assert matching_events

    assert (
        matching_events[-1].get("result")
        == "SUCCESS"
    )

    assert (
        matching_events[-1].get("resource")
        == str(file_path)
    )