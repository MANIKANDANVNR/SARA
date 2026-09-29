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
        calculator_permission=False
    ):

        self.state = SimpleNamespace(
            authenticated=authenticated,
            emergency_shutdown=emergency_shutdown
        )

        self.audit = FakeAuditLogger()

        self.calculator_permission = (
            calculator_permission
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
            == PermissionType.CALCULATOR
        ):

            return (
                self.calculator_permission
            )

        return False

    def logout(self):

        self.state.authenticated = False

        self.calculator_permission = False

    def revoke_all_permissions(self):

        self.calculator_permission = False

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


class FakeTool:

    name = "calculator"

    description = (
        "Fake calculator for controller tests."
    )

    def execute(self, expression):

        if expression == "2 + 2":

            return 4

        if expression == "10 * 5":

            return 50

        if expression == "invalid":

            raise ValueError(
                "Invalid mathematical expression."
            )

        raise ValueError(
            "Unsupported test expression."
        )


def create_controller(
    authenticated=False,
    emergency_shutdown=False,
    calculator_permission=False
):

    security = FakeSecurityManager(
        authenticated=authenticated,
        emergency_shutdown=emergency_shutdown,
        calculator_permission=calculator_permission
    )

    tools = SimpleNamespace()

    tools.tools = {
        "calculator": FakeTool()
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


def test_calculator_execution_requires_authentication():

    controller, security = create_controller(
        authenticated=False,
        calculator_permission=True
    )

    result = controller.execute_calculator(
        "2 + 2"
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


def test_calculator_execution_requires_permission():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=False
    )

    result = controller.execute_calculator(
        "2 + 2"
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Tool execution permission denied."
    )


def test_calculator_executes_with_authentication_and_permission():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    result = controller.execute_calculator(
        "2 + 2"
    )

    assert result["success"] is True

    assert result["result"] == 4

    assert result["error"] is None

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "SUCCESS"
    )


def test_calculator_returns_correct_result():

    controller, _ = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    result = controller.execute_calculator(
        "10 * 5"
    )

    assert result["success"] is True

    assert result["result"] == 50


def test_invalid_calculation_is_rejected_safely():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    result = controller.execute_calculator(
        "invalid"
    )

    assert result["success"] is False

    assert result["result"] is None

    assert (
        result["error"]
        == "Invalid mathematical expression."
    )

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "FAILED"
    )


def test_unknown_tool_is_rejected():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    result = controller.execute_tool(
        tool_name="unknown_tool",
        permission_type=PermissionType.CALCULATOR,
        level=PermissionLevel.LOW
    )

    assert result["success"] is False

    assert result["result"] is None

    assert result["error"] == "Tool not found."

    assert (
        security.audit.events[-1]["event"]
        == "TOOL_EXECUTION"
    )

    assert (
        security.audit.events[-1]["result"]
        == "TOOL_NOT_FOUND"
    )


def test_tool_execution_is_audit_logged():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    result = controller.execute_calculator(
        "2 + 2"
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
        == "calculator"
    )

    assert (
        execution_events[0]["result"]
        == "SUCCESS"
    )


def test_logout_removes_calculator_permission():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    first_result = controller.execute_calculator(
        "2 + 2"
    )

    assert first_result["success"] is True

    controller.logout()

    assert security.state.authenticated is False

    assert (
        security.calculator_permission
        is False
    )

    second_result = controller.execute_calculator(
        "2 + 2"
    )

    assert second_result["success"] is False


def test_emergency_shutdown_blocks_calculator():

    controller, security = create_controller(
        authenticated=True,
        emergency_shutdown=True,
        calculator_permission=True
    )

    result = controller.execute_calculator(
        "2 + 2"
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