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

    def request_permission(
        self,
        permission_type,
        level,
        resource=None,
        duration=None
    ):

        if not self.state.authenticated:

            return False

        if (
            permission_type
            == PermissionType.CALCULATOR
            and level
            == PermissionLevel.LOW
        ):

            self.calculator_permission = True

            return True

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
            "authentication_level": "BASIC"
            if self.state.authenticated
            else "NONE",
            "active_permissions": (
                ["calculator"]
                if self.calculator_permission
                else []
            ),
            "emergency_shutdown": (
                self.state.emergency_shutdown
            )
        }

    def emergency_shutdown(self):

        self.state.emergency_shutdown = True

        self.state.authenticated = False

        self.calculator_permission = False


class FakeCalculatorTool:

    name = "calculator"

    description = (
        "Fake calculator for controller tests."
    )

    def execute(self, expression):

        if expression == "25 * 8":

            return 200

        if expression == "(100 + 50) / 5":

            return 30

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
        "calculator": FakeCalculatorTool()
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


def test_calculate_command_requires_authentication():

    controller, security = create_controller(
        authenticated=False
    )

    response = controller.handle_command(
        "calculate 25 * 8"
    )

    assert (
        response
        == (
            "Permission denied. "
            "Authentication required "
            "to use the calculator."
        )
    )

    assert (
        security.calculator_permission
        is False
    )


def test_calculate_command_automatically_requests_low_permission():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=False
    )

    response = controller.handle_command(
        "calculate 25 * 8"
    )

    assert response == "Result: 200"

    assert (
        security.calculator_permission
        is True
    )


def test_calculate_command_executes_with_existing_permission():

    controller, security = create_controller(
        authenticated=True,
        calculator_permission=True
    )

    response = controller.handle_command(
        "calculate 25 * 8"
    )

    assert response == "Result: 200"

    assert (
        security.calculator_permission
        is True
    )


def test_calculate_command_handles_parentheses():

    controller, _ = create_controller(
        authenticated=True
    )

    response = controller.handle_command(
        "calculate (100 + 50) / 5"
    )

    assert response == "Result: 30"


def test_calculate_command_rejects_invalid_expression():

    controller, _ = create_controller(
        authenticated=True
    )

    response = controller.handle_command(
        "calculate invalid"
    )

    assert (
        response
        == (
            "Calculation failed: "
            "Invalid mathematical expression."
        )
    )


def test_calculate_command_is_case_insensitive():

    controller, _ = create_controller(
        authenticated=True
    )

    response = controller.handle_command(
        "CALCULATE 25 * 8"
    )

    assert response == "Result: 200"


def test_calculate_command_creates_audit_event():

    controller, security = create_controller(
        authenticated=True
    )

    response = controller.handle_command(
        "calculate 25 * 8"
    )

    assert response == "Result: 200"

    events = [
        event
        for event in security.audit.events
        if event["event"]
        == "CALCULATOR_REQUEST"
    ]

    assert len(events) == 1

    assert (
        events[0]["action"]
        == "calculate"
    )

    assert (
        events[0]["resource"]
        == "calculator"
    )

    assert (
        events[0]["result"]
        == "SUCCESS"
    )


def test_logout_removes_calculator_access():

    controller, security = create_controller(
        authenticated=True
    )

    first_response = (
        controller.handle_command(
            "calculate 25 * 8"
        )
    )

    assert first_response == "Result: 200"

    assert (
        security.calculator_permission
        is True
    )

    controller.logout()

    assert (
        security.state.authenticated
        is False
    )

    assert (
        security.calculator_permission
        is False
    )

    second_response = (
        controller.handle_command(
            "calculate 25 * 8"
        )
    )

    assert (
        second_response
        == (
            "Permission denied. "
            "Authentication required "
            "to use the calculator."
        )
    )


def test_emergency_shutdown_blocks_calculator():

    controller, security = create_controller(
        authenticated=True,
        emergency_shutdown=True
    )

    response = controller.handle_command(
        "calculate 25 * 8"
    )

    assert (
        response
        == (
            "Permission denied. "
            "Emergency shutdown is active."
        )
    )

    assert (
        security.calculator_permission
        is False
    )

    assert (
        security.audit.events[-1]["event"]
        == "CALCULATOR_REQUEST"
    )

    assert (
        security.audit.events[-1]["result"]
        == "EMERGENCY_SHUTDOWN"
    )