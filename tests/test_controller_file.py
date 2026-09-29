from pathlib import Path
from types import SimpleNamespace

from core.controller import SaraController

from security.permission import (
    PermissionType,
    PermissionLevel
)


class FakeAuditLogger:

    def __init__(self):

        self.events = []

    def record(
        self,
        event,
        action=None,
        resource=None,
        result=None
    ):

        self.events.append({
            "event": event,
            "action": action,
            "resource": resource,
            "result": result
        })


class FakeSecurityManager:

    def __init__(
        self,
        authenticated=False,
        file_permissions=None,
        emergency_shutdown=False
    ):

        self.state = SimpleNamespace(
            authenticated=authenticated,
            emergency_shutdown=emergency_shutdown
        )

        self.audit = FakeAuditLogger()

        self.file_permissions = (
            set(file_permissions or [])
        )

    def is_authenticated(self):

        return self.state.authenticated

    def has_permission(
        self,
        permission_type,
        resource=None
    ):

        if (
            permission_type
            == PermissionType.READ_FILE
        ):

            return (
                resource
                in self.file_permissions
            )

        return False

    def logout(self):

        self.state.authenticated = False

        self.file_permissions.clear()

    def revoke_all_permissions(self):

        self.file_permissions.clear()

    def get_security_status(self):

        return {
            "authenticated": (
                self.state.authenticated
            ),
            "authentication_level": "NONE",
            "active_permissions": [],
            "emergency_shutdown": (
                self.state.emergency_shutdown
            )
        }


class FakeFileTool:

    name = "file"

    description = (
        "Fake file tool for controller tests."
    )

    def execute(
        self,
        path,
        encoding=None
    ):

        file_path = Path(path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():

            raise ValueError(
                "The specified path is not a file."
            )

        selected_encoding = (
            encoding
            if encoding
            else "utf-8"
        )

        return file_path.read_text(
            encoding=selected_encoding
        )


def create_controller(
    authenticated=False,
    file_permissions=None,
    emergency_shutdown=False
):

    security = FakeSecurityManager(
        authenticated=authenticated,
        file_permissions=file_permissions,
        emergency_shutdown=emergency_shutdown
    )

    tools = SimpleNamespace()

    tools.tools = {
        "file": FakeFileTool()
    }

    tools.get = (
        lambda name:
        tools.tools.get(
            str(name).strip().lower()
        )
    )

    tools.exists = (
        lambda name:
        str(name).strip().lower()
        in tools.tools
    )

    tools.list_tools = (
        lambda:
        list(tools.tools.keys())
    )

    controller = SaraController(
        sara=SimpleNamespace(
            version="0.8.0"
        ),
        state=security.state,
        security=security,
        brain=SimpleNamespace(),
        memory=SimpleNamespace(),
        context=SimpleNamespace(),
        conversation=SimpleNamespace(),
        memory_store=SimpleNamespace(),
        conversation_store=SimpleNamespace(),
        profile=SimpleNamespace(),
        profile_store=SimpleNamespace(),
        tools=tools,
        voice=SimpleNamespace(),
        ui=SimpleNamespace()
    )

    return controller, security


def test_file_execution_requires_authentication(
    tmp_path
):

    file_path = (
        tmp_path
        / "test.txt"
    )

    file_path.write_text(
        "Hello SARA",
        encoding="utf-8"
    )

    controller, security = create_controller(
        authenticated=False,
        file_permissions=[
            str(file_path)
        ]
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )


def test_file_execution_requires_permission(
    tmp_path
):

    file_path = (
        tmp_path
        / "test.txt"
    )

    file_path.write_text(
        "Hello SARA",
        encoding="utf-8"
    )

    controller, security = create_controller(
        authenticated=True,
        file_permissions=[]
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert (
        security.audit.events[-1]["result"]
        == "PERMISSION_DENIED"
    )


def test_file_execution_requires_exact_resource_permission(
    tmp_path
):

    allowed_file = (
        tmp_path
        / "allowed.txt"
    )

    other_file = (
        tmp_path
        / "other.txt"
    )

    allowed_file.write_text(
        "Allowed",
        encoding="utf-8"
    )

    other_file.write_text(
        "Other",
        encoding="utf-8"
    )

    controller, _ = create_controller(
        authenticated=True,
        file_permissions=[
            str(allowed_file)
        ]
    )

    result = controller.execute_file(
        str(other_file)
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool execution permission denied."
    )


def test_file_executes_with_authentication_and_permission(
    tmp_path
):

    file_path = (
        tmp_path
        / "test.txt"
    )

    file_path.write_text(
        "Hello SARA",
        encoding="utf-8"
    )

    controller, security = create_controller(
        authenticated=True,
        file_permissions=[
            str(file_path)
        ]
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is True

    assert result["result"] == "Hello SARA"

    assert result["error"] is None

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "SUCCESS"
    )


def test_file_returns_multiline_content(
    tmp_path
):

    file_path = (
        tmp_path
        / "notes.txt"
    )

    content = (
        "Line 1\n"
        "Line 2\n"
        "Line 3"
    )

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    controller, _ = create_controller(
        authenticated=True,
        file_permissions=[
            str(file_path)
        ]
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is True

    assert result["result"] == content


def test_file_supports_custom_encoding(
    tmp_path
):

    file_path = (
        tmp_path
        / "latin.txt"
    )

    content = "café"

    file_path.write_text(
        content,
        encoding="latin-1"
    )

    controller, _ = create_controller(
        authenticated=True,
        file_permissions=[
            str(file_path)
        ]
    )

    result = controller.execute_file(
        str(file_path),
        encoding="latin-1"
    )

    assert result["success"] is True

    assert result["result"] == content


def test_missing_file_returns_failure(
    tmp_path
):

    file_path = (
        tmp_path
        / "missing.txt"
    )

    controller, security = create_controller(
        authenticated=True,
        file_permissions=[
            str(file_path)
        ]
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        "File not found"
        in result["error"]
    )

    assert (
        security.audit.events[-1]["result"]
        == "FAILED"
    )


def test_directory_returns_failure(
    tmp_path
):

    directory = (
        tmp_path
        / "folder"
    )

    directory.mkdir()

    controller, security = create_controller(
        authenticated=True,
        file_permissions=[
            str(directory)
        ]
    )

    result = controller.execute_file(
        str(directory)
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "The specified path is not a file."
    )

    assert (
        security.audit.events[-1]["result"]
        == "FAILED"
    )


def test_file_permission_resource_is_passed_to_security(
    tmp_path
):

    file_path = (
        tmp_path
        / "resource.txt"
    )

    file_path.write_text(
        "Resource test",
        encoding="utf-8"
    )

    controller, security = create_controller(
        authenticated=True,
        file_permissions=[
            str(file_path)
        ]
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is True

    assert (
        security.audit.events[-1]["resource"]
        == str(file_path)
    )


def test_unknown_file_tool_returns_failure(
    tmp_path
):

    file_path = (
        tmp_path
        / "test.txt"
    )

    file_path.write_text(
        "Hello",
        encoding="utf-8"
    )

    controller, security = create_controller(
        authenticated=True,
        file_permissions=[
            str(file_path)
        ]
    )

    controller.tools.tools.pop(
        "file"
    )

    result = controller.execute_file(
        str(file_path)
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool not found."
    )

    assert (
        security.audit.events[-1]["result"]
        == "TOOL_NOT_FOUND"
    )