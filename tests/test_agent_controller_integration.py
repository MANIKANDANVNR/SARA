from types import SimpleNamespace

from agent.runner import AgentRunner
from agent.step import AgentStep
from agent.task import AgentTask

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

    def __init__(self):
        self.state = SimpleNamespace(
            authenticated=True,
            emergency_shutdown=False
        )

        self.audit = FakeAuditLogger()
        self.calculator_permission = True

    def is_authenticated(self):
        return self.state.authenticated

    def has_permission(
        self,
        permission_type,
        resource=None
    ):
        if permission_type == PermissionType.CALCULATOR:
            return self.calculator_permission

        return False

    def revoke_all_permissions(self):
        self.calculator_permission = False

    def logout(self):
        self.state.authenticated = False
        self.calculator_permission = False


class FakeCalculatorTool:

    name = "calculator"

    description = (
        "Fake calculator for agent integration tests."
    )

    def execute(self, expression):

        if expression == "10 + 5":
            return 15

        if expression == "20 * 3":
            return 60

        raise ValueError(
            "Unsupported test expression."
        )


def create_controller():

    security = FakeSecurityManager()

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
            version="0.9.0"
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


def test_agent_runner_executes_multiple_steps_through_controller():

    controller, security = create_controller()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request=(
            "Calculate 10 + 5 and then "
            "calculate 20 * 3."
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "10 + 5"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "20 * 3"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == "completed"
    assert result.current_step == 2
    assert result.result == 60
    assert result.error is None

    assert task.steps[0].status == "success"
    assert task.steps[0].result == 15

    assert task.steps[1].status == "success"
    assert task.steps[1].result == 60

    execution_events = [
        event
        for event in security.audit.events
        if event["event"] == "TOOL_EXECUTION"
    ]

    assert len(execution_events) == 2

    assert execution_events[0]["action"] == "calculator"
    assert execution_events[1]["action"] == "calculator"

    assert execution_events[0]["result"] == "SUCCESS"
    assert execution_events[1]["result"] == "SUCCESS"


def test_agent_runner_is_blocked_by_controller_security():

    controller, security = create_controller()

    security.calculator_permission = False

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Calculate 10 + 5."
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "10 + 5"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == "failed"

    assert result.error == (
        "Tool execution permission denied."
    )

    assert result.current_step == 0

    assert task.steps[0].status == "failed"
    assert task.steps[0].attempts == 1
    assert task.steps[0].result is None


def test_handle_agent_runs_agent_task_through_controller():

    controller, security = create_controller()

    task = AgentTask(
        request="Calculate 10 + 5."
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "10 + 5"
            }
        )
    )

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            assert request == "Calculate 10 + 5."
            return task

    class FakeAgentRunner:

        def run(
            self,
            task,
            permission_type=None,
            level=None
        ):
            assert permission_type is None
            assert level is None

            task.status = "completed"
            task.result = 15
            task.report = (
                "Task completed successfully "
                "with 1 step(s)."
            )

            return task

    controller.agent = FakeAgent()
    controller.agent_runner = FakeAgentRunner()

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == "15"

    assert task.status == "completed"
    assert task.result == 15

    assert task.report == (
        "Task completed successfully "
        "with 1 step(s)."
    )


def test_handle_agent_requires_authentication():

    controller, security = create_controller()

    security.state.authenticated = False

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            raise AssertionError(
                "Agent planning should not run "
                "without authentication."
            )

    controller.agent = FakeAgent()

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == (
        "Permission denied. "
        "Authentication required "
        "to use agent mode."
    )


def test_handle_agent_requires_agent():

    controller, security = create_controller()

    security.state.authenticated = True
    controller.agent = None

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == "Agent is not available."


def test_handle_agent_requires_agent_runner():

    controller, security = create_controller()

    security.state.authenticated = True

    controller.agent = SimpleNamespace(
        create_plan=lambda request, context=None:
        AgentTask(
            request=request
        )
    )

    controller.agent_runner = None

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == (
        "Agent runner is not available."
    )


def test_handle_agent_handles_planning_failure():

    controller, security = create_controller()

    security.state.authenticated = True

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            raise RuntimeError(
                "Planning service failed."
            )

    controller.agent = FakeAgent()

    controller.agent_runner = SimpleNamespace()

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == (
        "Agent planning failed: "
        "Planning service failed."
    )

    planning_events = [
        event
        for event in security.audit.events
        if event["event"] == "AGENT_PLAN_FAILED"
    ]

    assert len(planning_events) == 1

    assert planning_events[0]["action"] == (
        "create_plan"
    )

    assert planning_events[0]["result"] == (
        "Planning service failed."
    )

def test_handle_agent_handles_execution_failure():

    controller, security = create_controller()

    security.state.authenticated = True

    task = AgentTask(
        request="Calculate 10 + 5."
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "10 + 5"
            }
        )
    )

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            return task

    class FakeAgentRunner:

        def run(
            self,
            task,
            permission_type=None,
            level=None
        ):
            task.status = "failed"
            task.error = (
                "Tool execution failed."
            )
            return task

    controller.agent = FakeAgent()
    controller.agent_runner = FakeAgentRunner()

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == (
        "Tool execution failed."
    )

    assert task.status == "failed"

    assert task.error == (
        "Tool execution failed."
    )

def test_handle_agent_does_not_run_after_planning_failure():

    controller, security = create_controller()

    security.state.authenticated = True

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            raise RuntimeError(
                "Planning service failed."
            )

    class FakeAgentRunner:

        def run(
            self,
            task,
            permission_type=None,
            level=None
        ):
            raise AssertionError(
                "Agent runner must not execute "
                "after planning failure."
            )

    controller.agent = FakeAgent()
    controller.agent_runner = FakeAgentRunner()

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == (
        "Agent planning failed: "
        "Planning service failed."
    )

def test_handle_agent_rejects_tool_without_security_policy():

    controller, security = create_controller()

    security.state.authenticated = True

    task = AgentTask(
        request="Run an unauthorized operation."
    )

    task.steps.append(
        AgentStep(
            tool_name="delete_everything",
            arguments={}
        )
    )

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            return task

    class FakeAgentRunner:

        def run(
            self,
            task,
            permission_type=None,
            level=None
        ):
            raise AssertionError(
                "Agent runner must not execute "
                "a tool without a security policy."
            )

    controller.agent = FakeAgent()
    controller.agent_runner = FakeAgentRunner()

    result = controller.handle_agent(
        "Run an unauthorized operation."
    )

    assert result == (
        "Security policy unavailable "
        "for tool 'delete_everything'."
    )

    assert task.status == "failed"

    assert task.error == (
        "Security policy unavailable "
        "for tool 'delete_everything'."
    )

    security_events = [
        event
        for event in security.audit.events
        if event["event"] == "AGENT_SECURITY_DENIED"
    ]

    assert len(security_events) == 1

    assert security_events[0]["action"] == (
        "delete_everything"
    )

    assert security_events[0]["result"] == (
        "POLICY_UNAVAILABLE"
    )

def test_agent_cannot_escalate_tool_permission_level():

    controller, security = create_controller()

    security.state.authenticated = True

    task = AgentTask(
        request="Calculate 10 + 5."
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "10 + 5"
            }
        )
    )

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            return task

    captured = {}

    original_execute_tool = (
        controller.execute_tool
    )

    def capture_execute_tool(
        tool_name,
        permission_type,
        level,
        *args,
        **kwargs
    ):
        captured["tool_name"] = tool_name
        captured["permission_type"] = permission_type
        captured["level"] = level

        return original_execute_tool(
            tool_name=tool_name,
            permission_type=permission_type,
            level=level,
            *args,
            **kwargs
        )

    controller.execute_tool = (
        capture_execute_tool
    )

    controller.agent = FakeAgent()

    controller.agent_runner = AgentRunner(
        controller
    )

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == "15"

    assert captured["tool_name"] == (
        "calculator"
    )

    assert captured["permission_type"] == (
        PermissionType.CALCULATOR
    )

    assert captured["level"] == (
        PermissionLevel.LOW
    )
def test_agent_cannot_change_tool_permission_type():

    controller, security = create_controller()

    security.state.authenticated = True

    task = AgentTask(
        request="Calculate 10 + 5."
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "10 + 5"
            }
        )
    )

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):
            return task

    captured = {}

    original_execute_tool = (
        controller.execute_tool
    )

    def capture_execute_tool(
        tool_name,
        permission_type,
        level,
        *args,
        **kwargs
    ):
        captured["tool_name"] = tool_name
        captured["permission_type"] = (
            permission_type
        )
        captured["level"] = level

        return original_execute_tool(
            tool_name=tool_name,
            permission_type=permission_type,
            level=level,
            *args,
            **kwargs
        )

    controller.execute_tool = (
        capture_execute_tool
    )

    controller.agent = FakeAgent()

    controller.agent_runner = AgentRunner(
        controller
    )

    result = controller.handle_agent(
        "Calculate 10 + 5."
    )

    assert result == "15"

    assert captured["tool_name"] == (
        "calculator"
    )

    assert captured["permission_type"] == (
        PermissionType.CALCULATOR
    )

    assert captured["permission_type"] != (
        PermissionType.SYSTEM
    )

    assert captured["level"] == (
        PermissionLevel.LOW
    )