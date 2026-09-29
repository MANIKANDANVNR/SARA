from agent.agent import SaraAgent
from agent.runner import AgentRunner
from agent.step import AgentStep
from agent.task import AgentTask

from brain.ollama import OllamaProvider

from core.controller import SaraController
from core.sara import Sara
from core.state import SaraState

from memory.context_manager import ContextManager
from memory.conversation_manager import ConversationManager
from memory.conversation_store import ConversationStore
from memory.memory_manager import MemoryManager
from memory.memory_store import MemoryStore
from memory.profile_manager import ProfileManager
from memory.profile_store import ProfileStore

from security.permission import (
    PermissionType,
    PermissionLevel
)

from security.security_manager import (
    SecurityManager
)

from tools.calculator import CalculatorTool
from tools.tool_registry import ToolRegistry

from types import SimpleNamespace


class FakeVoice:

    pass


class FakeUI:

    pass


class RetryCalculatorController:

    def __init__(
        self,
        controller
    ):

        self.controller = controller

        self.failed_once = False

    def execute_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        **kwargs
    ):

        if (
            tool_name == "calculator"
            and kwargs.get("expression") == "100 + 50"
            and not self.failed_once
        ):

            self.failed_once = True

            return {
                "success": False,
                "result": None,
                "error": "execution failed."
            }

        return self.controller.execute_tool(
            tool_name=tool_name,
            permission_type=permission_type,
            level=level,
            resource=resource,
            **kwargs
        )


class AlwaysFailCalculatorController:

    def __init__(
        self,
        controller
    ):

        self.controller = controller

    def execute_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        **kwargs
    ):

        if (
            tool_name == "calculator"
            and kwargs.get("expression") == "100 + 50"
        ):

            return {
                "success": False,
                "result": None,
                "error": "execution failed."
            }

        return self.controller.execute_tool(
            tool_name=tool_name,
            permission_type=permission_type,
            level=level,
            resource=resource,
            **kwargs
        )


def create_real_controller():

    state = SaraState()

    security = SecurityManager(
        state
    )

    sara = Sara(
        security
    )

    memory = MemoryManager(
        max_short_term=10
    )

    memory_store = MemoryStore(
        "test_agent_real_memory.json"
    )

    conversation = ConversationManager(
        max_messages=20
    )

    conversation_store = ConversationStore(
        "test_agent_real_conversation.json"
    )

    profile = ProfileManager()

    profile_store = ProfileStore(
        "test_agent_real_profile.json"
    )

    context = ContextManager(
        memory_manager=memory,
        conversation_manager=conversation,
        profile_manager=profile,
        max_recent_messages=10,
        max_long_term_memories=10
    )

    tools = ToolRegistry()

    calculator = CalculatorTool()

    tools.register(
        calculator.name,
        calculator
    )

    controller = SaraController(
        sara=sara,
        state=state,
        security=security,
        brain=SimpleNamespace(),
        memory=memory,
        context=context,
        conversation=conversation,
        memory_store=memory_store,
        conversation_store=conversation_store,
        profile=profile,
        profile_store=profile_store,
        tools=tools,
        voice=FakeVoice(),
        ui=FakeUI()
    )

    return controller


def create_real_agent():

    provider = OllamaProvider(
        model="qwen2.5:3b",
        timeout=120
    )

    registry = ToolRegistry()

    calculator = CalculatorTool()

    registry.register(
        calculator.name,
        calculator
    )

    return SaraAgent(
        provider=provider,
        tool_registry=registry
    )


def authorize_calculator(
    controller
):

    controller.security.authenticate()

    controller.security.request_permission(
        PermissionType.CALCULATOR,
        PermissionLevel.LOW,
        duration=60
    )


def test_real_ollama_agent_executes_through_real_controller():

    agent = create_real_agent()

    task = agent.create_plan(
        "Calculate 25 * 4 using the calculator."
    )

    assert len(
        task.steps
    ) >= 1

    assert task.steps[0].tool_name == (
        "calculator"
    )

    controller = create_real_controller()

    authorize_calculator(
        controller
    )

    runner = AgentRunner(
        controller
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == (
        len(task.steps)
    )

    assert result.result == 100

    assert result.error is None

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == 100


def test_real_ollama_agent_executes_multiple_steps_through_real_controller():

    agent = create_real_agent()

    task = agent.create_plan(
        "Calculate 25 * 4 and then calculate 100 + 50."
    )

    assert len(
        task.steps
    ) >= 2

    assert task.steps[0].tool_name == (
        "calculator"
    )

    assert task.steps[1].tool_name == (
        "calculator"
    )

    assert task.steps[0].arguments[
        "expression"
    ] == "25 * 4"

    assert task.steps[1].arguments[
        "expression"
    ] == "100 + 50"

    controller = create_real_controller()

    authorize_calculator(
        controller
    )

    runner = AgentRunner(
        controller
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == (
        len(task.steps)
    )

    assert result.result == 150

    assert result.error is None

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == 100

    assert task.steps[1].status == (
        "success"
    )

    assert task.steps[1].result == 150


def test_real_ollama_agent_is_blocked_by_real_controller_security():

    agent = create_real_agent()

    task = agent.create_plan(
        "Calculate 25 * 4 using the calculator."
    )

    assert len(
        task.steps
    ) >= 1

    assert task.steps[0].tool_name == (
        "calculator"
    )

    controller = create_real_controller()

    runner = AgentRunner(
        controller
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "failed"
    )

    assert result.error == (
        "Tool execution permission denied."
    )

    assert result.current_step == 0

    assert task.steps[0].status == (
        "failed"
    )

    assert task.steps[0].attempts == 1

    assert task.steps[0].result is None


def test_real_multi_step_execution_stops_after_step_failure():

    controller = create_real_controller()

    authorize_calculator(
        controller
    )

    task = AgentTask(
        request=(
            "Execute three calculator operations "
            "and stop if any operation fails."
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 / 0"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "100 + 50"
            }
        )
    )

    runner = AgentRunner(
        controller
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "failed"
    )

    assert result.current_step == 1

    assert result.result is None

    assert result.error is not None

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == 100

    assert task.steps[0].attempts == 1

    assert task.steps[1].status == (
        "failed"
    )

    assert task.steps[1].attempts == 1

    assert task.steps[1].result is None

    assert task.steps[2].status == (
        "pending"
    )

    assert task.steps[2].attempts == 0

    assert task.steps[2].result is None


def test_real_multi_step_execution_retries_temporary_failure():

    controller = create_real_controller()

    authorize_calculator(
        controller
    )

    retry_controller = RetryCalculatorController(
        controller
    )

    task = AgentTask(
        request=(
            "Execute three calculator operations "
            "and retry temporary failures."
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "100 + 50"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "200 - 50"
            }
        )
    )

    runner = AgentRunner(
        retry_controller
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == 3

    assert result.result == 150

    assert result.error is None

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == 100

    assert task.steps[0].attempts == 1

    assert task.steps[1].status == (
        "success"
    )

    assert task.steps[1].result == 150

    assert task.steps[1].attempts == 2

    assert task.steps[2].status == (
        "success"
    )

    assert task.steps[2].result == 150

    assert task.steps[2].attempts == 1


def test_real_multi_step_execution_stops_after_max_retries():

    controller = create_real_controller()

    authorize_calculator(
        controller
    )

    failing_controller = AlwaysFailCalculatorController(
        controller
    )

    task = AgentTask(
        request=(
            "Execute three calculator operations "
            "and stop after maximum retries."
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "100 + 50"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "200 - 50"
            }
        )
    )

    runner = AgentRunner(
        failing_controller
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "failed"
    )

    assert result.current_step == 1

    assert result.error == (
        "execution failed."
    )

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == 100

    assert task.steps[0].attempts == 1

    assert task.steps[1].status == (
        "failed"
    )

    assert task.steps[1].attempts == 3

    assert task.steps[1].result is None

    assert task.steps[2].status == (
        "pending"
    )

    assert task.steps[2].attempts == 0

    assert task.steps[2].result is None

def test_real_multi_step_execution_fails_when_verification_fails():
        controller = create_real_controller()

        authorize_calculator(
            controller
        )

        task = AgentTask(
            request=(
                "Execute a calculator operation "
                "and verify the result."
            )
        )

        task.steps.append(
            AgentStep(
                tool_name="calculator",
                arguments={
                    "expression": "25 * 4"
                }
            )
        )

        class RejectingVerifier:

            def verify(
                    self,
                    task
            ):
                return False

        runner = AgentRunner(
            controller,
            verifier=RejectingVerifier()
        )

        result = runner.run(
            task=task,
            permission_type=None,
            level=None
        )

        assert result.status == (
            "failed"
        )

        assert result.error == (
            "Task verification failed."
        )

        assert result.current_step == 1

        assert task.steps[0].status == (
            "success"
        )

        assert task.steps[0].result == 100

        assert task.steps[0].attempts == 1


def test_real_ollama_agent_executes_through_handle_agent():
    controller = create_real_controller()

    authorize_calculator(
        controller
    )

    controller.agent = create_real_agent()

    controller.agent_runner = AgentRunner(
        controller
    )

    result = controller.handle_agent(
        "Calculate 25 * 4 using the calculator."
    )

    assert result == "100"

def test_handle_agent_stops_when_tool_permission_is_denied():

    controller = create_real_controller()

    controller.security.authenticate()

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):

            task = AgentTask(
                request=request
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

    class FailingRunner:

        def __init__(self):

            self.called = False

        def run(
            self,
            task,
            permission_type,
            level
        ):

            self.called = True

            raise AssertionError(
                "AgentRunner must not execute "
                "when permission is denied."
            )

    controller.agent = FakeAgent()

    runner = FailingRunner()

    controller.agent_runner = runner

    controller.request_tool_access = (
        lambda **kwargs: False
    )

    result = controller.handle_agent(
        "Calculate 25 * 4 using the calculator."
    )

    assert result == (
        "Agent permission denied "
        "for tool 'calculator'."
    )

    assert runner.called is False

def test_handle_agent_is_blocked_without_authorization():

    controller = create_real_controller()

    controller.agent = create_real_agent()

    controller.agent_runner = AgentRunner(
        controller
    )

    result = controller.handle_agent(
        "Calculate 25 * 4 using the calculator."
    )

    assert result == (
        "Permission denied. "
        "Authentication required "
        "to use agent mode."
    )

def test_handle_agent_rejects_tool_without_security_policy():

    controller = create_real_controller()

    controller.security.authenticate()

    class FakeAgent:

        def create_plan(
            self,
            request,
            context=None
        ):

            task = AgentTask(
                request=request
            )

            task.steps.append(
                AgentStep(
                    tool_name="unknown_dangerous_tool",
                    arguments={}
                )
            )

            return task

    class FailingRunner:

        def __init__(self):

            self.called = False

        def run(
            self,
            task,
            permission_type,
            level
        ):

            self.called = True

            raise AssertionError(
                "AgentRunner must not execute "
                "a tool without a security policy."
            )

    controller.agent = FakeAgent()

    runner = FailingRunner()

    controller.agent_runner = runner

    result = controller.handle_agent(
        "Execute an unknown tool."
    )

    assert result == (
        "Security policy unavailable "
        "for tool 'unknown_dangerous_tool'."
    )

    assert runner.called is False

def test_real_agent_sequential_calculation_with_three_operations():
    controller = create_real_controller()
    authorize_calculator(controller)

    controller.agent = create_real_agent()
    controller.agent_runner = AgentRunner(controller)

    result = controller.handle_agent(
        "Calculate 157 * 83, divide by 7, add 1234, "
        "use appropriate tool each step."
    )

    assert result == "3095.5714285714284"

def test_real_agent_sequential_calculation_using_previous_result():
    controller = create_real_controller()
    authorize_calculator(controller)

    controller.agent = create_real_agent()
    controller.agent_runner = AgentRunner(controller)

    result = controller.handle_agent(
        "First calculate 157 * 83. "
        "Then take that result and divide by 7."
    )

    assert result == "1861.5714285714287"