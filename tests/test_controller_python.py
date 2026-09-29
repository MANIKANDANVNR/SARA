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
        emergency_shutdown=False,
        python_permission=False
    ):

        self.state = SimpleNamespace(
            authenticated=authenticated,
            emergency_shutdown=emergency_shutdown
        )

        self.audit = FakeAuditLogger()

        self.python_permission = (
            python_permission
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
            == PermissionType.PYTHON
        ):

            return self.python_permission

        return False

    def request_permission(
        self,
        permission_type,
        level,
        resource=None,
        duration=None
    ):

        if (
            permission_type
            == PermissionType.PYTHON
        ):

            self.python_permission = True

            return True

        return False

    def logout(self):

        self.state.authenticated = False

        self.python_permission = False

    def revoke_all_permissions(self):

        self.python_permission = False

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


class FakePythonTool:

    name = "python"

    description = (
        "Fake Python executor for controller tests."
    )

    def execute(self, code):

        if code == "10 + 20":

            return 30

        if code == "print(25 * 4)":

            return "100"

        if code == "invalid":

            raise ValueError(
                "Invalid Python syntax."
            )

        raise ValueError(
            "Unsupported test code."
        )


def create_controller(
    authenticated=False,
    emergency_shutdown=False,
    python_permission=False
):

    security = FakeSecurityManager(
        authenticated=authenticated,
        emergency_shutdown=emergency_shutdown,
        python_permission=python_permission
    )

    tools = SimpleNamespace()

    tools.tools = {
        "python": FakePythonTool()
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


# =================================================
# AUTHENTICATION
# =================================================


def test_python_execution_requires_authentication():

    controller, security = create_controller(
        authenticated=False,
        python_permission=True
    )

    result = controller.execute_python(
        "10 + 20"
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


# =================================================
# PERMISSION
# =================================================


def test_python_execution_requires_permission():

    controller, security = create_controller(
        authenticated=True,
        python_permission=False
    )

    result = controller.execute_python(
        "10 + 20"
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool execution permission denied."
    )


# =================================================
# EXECUTION
# =================================================


def test_python_executes_with_permission():

    controller, security = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.execute_python(
        "10 + 20"
    )

    assert result["success"] is True

    assert result["result"] == 30

    assert result["error"] is None

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "SUCCESS"
    )


def test_python_returns_correct_result():

    controller, _ = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.execute_python(
        "print(25 * 4)"
    )

    assert result["success"] is True

    assert result["result"] == "100"


# =================================================
# ERROR HANDLING
# =================================================


def test_python_execution_returns_tool_error():

    controller, security = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.execute_python(
        "invalid"
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Invalid Python syntax."
    )

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "FAILED"
    )


# =================================================
# TOOL NOT FOUND
# =================================================


def test_python_execution_rejects_missing_tool():

    controller, security = create_controller(
        authenticated=True,
        python_permission=True
    )

    controller.tools.tools.pop(
        "python"
    )

    result = controller.execute_python(
        "10 + 20"
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool not found."
    )

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "TOOL_NOT_FOUND"
    )


# =================================================
# EMERGENCY SHUTDOWN
# =================================================


def test_python_execution_is_blocked_during_emergency_shutdown():

    controller, security = create_controller(
        authenticated=True,
        emergency_shutdown=True,
        python_permission=True
    )

    result = controller.execute_python(
        "10 + 20"
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


# =================================================
# LOGGING
# =================================================


def test_python_tool_execution_is_audit_logged():

    controller, security = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.execute_python(
        "10 + 20"
    )

    assert result["success"] is True

    execution_events = [
        event
        for event in security.audit.events
        if event["event"] == "TOOL_EXECUTION"
    ]

    assert len(execution_events) == 1

    assert (
        execution_events[0]["action"]
        == "python"
    )

    assert (
        execution_events[0]["result"]
        == "SUCCESS"
    )


# =================================================
# HANDLE PYTHON
# =================================================


def test_handle_python_requires_authentication():

    controller, _ = create_controller(
        authenticated=False,
        python_permission=True
    )

    result = controller.handle_python(
        "10 + 20"
    )

    assert (
        result
        == (
            "Permission denied. "
            "Authentication required "
            "to use Python execution."
        )
    )


def test_handle_python_executes_successfully():

    controller, _ = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.handle_python(
        "10 + 20"
    )

    assert result == (
        "Python result:\n"
        "30"
    )


def test_handle_python_rejects_empty_code():

    controller, _ = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.handle_python(
        ""
    )

    assert (
        result
        == "Python code cannot be empty."
    )


# =================================================
# COMMAND ROUTING
# =================================================


def test_handle_command_routes_python():

    controller, _ = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.handle_command(
        "python 10 + 20"
    )

    assert result == (
        "Python result:\n"
        "30"
    )


def test_handle_command_routes_python_print():

    controller, _ = create_controller(
        authenticated=True,
        python_permission=True
    )

    result = controller.handle_command(
        "python print(25 * 4)"
    )

    assert result == (
        "Python result:\n"
        "100"
    )