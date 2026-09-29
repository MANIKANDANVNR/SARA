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
        action,
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

    def __init__(self):

        self.authenticated = False

        self.emergency_shutdown = False

        self.file_write_permissions = set()

        self.audit = FakeAuditLogger()

    def is_authenticated(self):

        return self.authenticated

    def get_authentication_level(self):

        return (
            PermissionLevel.MEDIUM
            if self.authenticated
            else None
        )

    def has_permission(
        self,
        permission_type,
        resource=None
    ):

        if permission_type == (
            PermissionType.WRITE_FILE
        ):

            return resource in (
                self.file_write_permissions
            )

        return False


class FakeSecurityGate:

    def __init__(self, security):

        self.security = security

    def authorize_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None
    ):

        if self.security.emergency_shutdown:

            return False

        if not self.security.authenticated:

            return False

        return self.security.has_permission(
            permission_type,
            resource
        )


class FakeFileWriteTool:

    name = "file_write"

    description = (
        "Fake file write tool for controller tests."
    )

    def __init__(self):

        self.calls = []

    def execute(
        self,
        path,
        content,
        encoding=None
    ):

        self.calls.append({
            "path": path,
            "content": content,
            "encoding": encoding
        })

        return str(path)


class FakeToolRegistry:

    def __init__(self, tools=None):

        self.tools = (
            tools
            if tools is not None
            else {}
        )

    def exists(self, name):

        return (
            name in self.tools
        )

    def get(self, name):

        return self.tools.get(
            name
        )


def create_controller(
    security,
    file_write_tool
):

    controller = object.__new__(
        SaraController
    )

    controller.security = security

    controller.security_gate = (
        FakeSecurityGate(
            security
        )
    )

    controller.tools = (
        FakeToolRegistry({
            "file_write": file_write_tool
        })
    )

    return controller


def test_unauthenticated_write_is_denied(
    tmp_path
):

    security = FakeSecurityManager()

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    file_path = (
        tmp_path /
        "test.txt"
    )

    result = controller.execute_file_write(
        file_path,
        "Hello SARA"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert tool.calls == []


def test_missing_write_permission_is_denied(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    file_path = (
        tmp_path /
        "test.txt"
    )

    result = controller.execute_file_write(
        file_path,
        "Hello SARA"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Tool execution permission denied."
    )

    assert tool.calls == []


def test_exact_resource_permission_is_required(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    first_path = (
        tmp_path /
        "allowed.txt"
    )

    second_path = (
        tmp_path /
        "blocked.txt"
    )

    security.file_write_permissions.add(
        first_path
    )

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    result = controller.execute_file_write(
        second_path,
        "Hello"
    )

    assert result["success"] is False

    assert tool.calls == []


def test_successful_write(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    file_path = (
        tmp_path /
        "test.txt"
    )

    security.file_write_permissions.add(
        file_path
    )

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    result = controller.execute_file_write(
        file_path,
        "Hello SARA"
    )

    assert result["success"] is True

    assert result["result"] == str(
        file_path
    )

    assert tool.calls == [
        {
            "path": file_path,
            "content": "Hello SARA",
            "encoding": None
        }
    ]


def test_multiline_content(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    file_path = (
        tmp_path /
        "multiline.txt"
    )

    security.file_write_permissions.add(
        file_path
    )

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    content = (
        "Line 1\n"
        "Line 2\n"
        "Line 3"
    )

    result = controller.execute_file_write(
        file_path,
        content
    )

    assert result["success"] is True

    assert tool.calls[0]["content"] == (
        content
    )


def test_custom_encoding(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    file_path = (
        tmp_path /
        "encoded.txt"
    )

    security.file_write_permissions.add(
        file_path
    )

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    result = controller.execute_file_write(
        file_path,
        "Hello",
        encoding="utf-16"
    )

    assert result["success"] is True

    assert tool.calls[0]["encoding"] == (
        "utf-16"
    )


def test_tool_failure_is_returned(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    file_path = (
        tmp_path /
        "test.txt"
    )

    security.file_write_permissions.add(
        file_path
    )

    class FailingTool:

        name = "file_write"

        def execute(
            self,
            path,
            content,
            encoding=None
        ):

            raise ValueError(
                "Unable to write the file."
            )

    controller = create_controller(
        security,
        FailingTool()
    )

    result = controller.execute_file_write(
        file_path,
        "Hello"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Unable to write the file."
    )


def test_resource_is_passed_to_security(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    file_path = (
        tmp_path /
        "test.txt"
    )

    security.file_write_permissions.add(
        file_path
    )

    tool = FakeFileWriteTool()

    controller = create_controller(
        security,
        tool
    )

    controller.execute_file_write(
        file_path,
        "Hello"
    )

    assert security.audit.events[-1][
        "resource"
    ] == file_path

    assert security.audit.events[-1][
        "action"
    ] == "file_write"


def test_unknown_tool_fails_safely(
    tmp_path
):

    security = FakeSecurityManager()

    security.authenticated = True

    controller = create_controller(
        security,
        FakeFileWriteTool()
    )

    controller.tools.tools = {}

    file_path = (
        tmp_path /
        "test.txt"
    )

    result = controller.execute_file_write(
        file_path,
        "Hello"
    )

    assert result["success"] is False

    assert (
        result["error"]
        == "Tool not found."
    )