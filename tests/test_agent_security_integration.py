from agent.runner import AgentRunner
from agent.step import AgentStep
from agent.task import AgentTask

from security.permission import (
    PermissionType,
    PermissionLevel
)

from security.security_gate import (
    SecurityGate
)


class MockAudit:

    def __init__(self):

        self.events = []

    def record(
        self,
        event,
        action,
        resource,
        result
    ):

        self.events.append(
            {
                "event": event,
                "action": action,
                "resource": resource,
                "result": result
            }
        )


class MockState:

    def __init__(self):

        self.emergency_shutdown = False


class MockSecurity:

    def __init__(self):

        self.state = MockState()

        self.audit = MockAudit()

        self.authenticated = False

        self.permissions = set()

    def is_authenticated(self):

        return self.authenticated

    def has_permission(
        self,
        permission_type,
        resource=None
    ):

        return permission_type in (
            self.permissions
        )


class SecurityController:

    def __init__(self):

        self.security = MockSecurity()

        self.security_gate = SecurityGate(
            self.security
        )

        self.executed = False

    def execute_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        **kwargs
    ):

        authorized = (
            self.security_gate.authorize_tool(
                tool_name=tool_name,
                permission_type=permission_type,
                level=level,
                resource=resource
            )
        )

        if not authorized:

            return {
                "success": False,
                "result": None,
                "error": (
                    "Tool execution "
                    "permission denied."
                )
            }

        self.executed = True

        return {
            "success": True,
            "result": "SECURE EXECUTION",
            "error": None
        }


class RetrySecurityController:

    def __init__(self):

        self.security = MockSecurity()

        self.security_gate = SecurityGate(
            self.security
        )

        self.calls = []

        self.security_checks = 0

    def execute_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        **kwargs
    ):

        authorized = (
            self.security_gate.authorize_tool(
                tool_name=tool_name,
                permission_type=permission_type,
                level=level,
                resource=resource
            )
        )

        self.security_checks += 1

        if not authorized:

            return {
                "success": False,
                "result": None,
                "error": (
                    "Tool execution "
                    "permission denied."
                )
            }

        self.calls.append(
            tool_name
        )

        if len(self.calls) < 3:

            return {
                "success": False,
                "result": None,
                "error": "Execution failed."
            }

        return {
            "success": True,
            "result": "SECURE RETRY EXECUTION",
            "error": None
        }


def create_task():

    task = AgentTask(
        request="Run calculator"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    return task


def test_agent_runner_respects_authentication():

    controller = SecurityController()

    runner = AgentRunner(
        controller
    )

    task = create_task()

    result = runner.run(
        task=task,
        permission_type=PermissionType.CALCULATOR,
        level=PermissionLevel.LOW
    )

    assert result.status == (
        "failed"
    )

    assert result.error == (
        "Tool execution permission denied."
    )

    assert controller.executed is False


def test_agent_runner_allows_authorized_execution():

    controller = SecurityController()

    controller.security.authenticated = True

    controller.security.permissions.add(
        PermissionType.CALCULATOR
    )

    runner = AgentRunner(
        controller
    )

    task = create_task()

    result = runner.run(
        task=task,
        permission_type=PermissionType.CALCULATOR,
        level=PermissionLevel.LOW
    )

    assert result.status == (
        "completed"
    )

    assert result.result == (
        "SECURE EXECUTION"
    )

    assert controller.executed is True


def test_agent_runner_respects_emergency_shutdown():

    controller = SecurityController()

    controller.security.authenticated = True

    controller.security.permissions.add(
        PermissionType.CALCULATOR
    )

    controller.security.state.emergency_shutdown = True

    runner = AgentRunner(
        controller
    )

    task = create_task()

    result = runner.run(
        task=task,
        permission_type=PermissionType.CALCULATOR,
        level=PermissionLevel.LOW
    )

    assert result.status == (
        "failed"
    )

    assert result.error == (
        "Tool execution permission denied."
    )

    assert controller.executed is False


def test_agent_runner_retries_through_security_boundary():

    controller = RetrySecurityController()

    controller.security.authenticated = True

    controller.security.permissions.add(
        PermissionType.CALCULATOR
    )

    runner = AgentRunner(
        controller
    )

    task = create_task()

    result = runner.run(
        task=task,
        permission_type=PermissionType.CALCULATOR,
        level=PermissionLevel.LOW
    )

    assert result.status == (
        "completed"
    )

    assert result.result == (
        "SECURE RETRY EXECUTION"
    )

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].attempts == 3

    assert task.steps[0].error is None

    assert controller.calls == [
        "calculator",
        "calculator",
        "calculator"
    ]

    assert controller.security_checks == 3