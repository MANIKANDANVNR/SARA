from agent.agent import SaraAgent

from agent.runner import AgentRunner

from brain.ollama import OllamaProvider

from tools.tool_registry import ToolRegistry

from tools.calculator import CalculatorTool


def create_agent():

    provider = OllamaProvider(
        model="qwen2.5:3b",
        timeout=120
    )

    registry = ToolRegistry()

    registry.register(
        "calculator",
        CalculatorTool()
    )

    return SaraAgent(
        provider=provider,
        tool_registry=registry
    )


def test_real_ollama_agent_creates_calculator_plan():

    agent = create_agent()

    task = agent.create_plan(
        "Calculate 25 * 4 using the calculator."
    )

    assert task.request == (
        "Calculate 25 * 4 using the calculator."
    )

    assert len(
        task.steps
    ) >= 1

    first_step = task.steps[0]

    assert first_step.tool_name == (
        "calculator"
    )

    assert first_step.arguments[
        "expression"
    ] == "25 * 4"


def test_real_ollama_agent_creates_multi_step_plan():

    agent = create_agent()

    task = agent.create_plan(
        "Calculate 25 * 4 and then calculate 100 + 50."
    )

    assert task.request == (
        "Calculate 25 * 4 and then calculate 100 + 50."
    )

    assert len(
        task.steps
    ) >= 2

    first_step = task.steps[0]
    second_step = task.steps[1]

    assert first_step.tool_name == (
        "calculator"
    )

    assert second_step.tool_name == (
        "calculator"
    )

    assert first_step.arguments[
        "expression"
    ] == "25 * 4"

    assert second_step.arguments[
        "expression"
    ] == "100 + 50"


def test_real_ollama_plan_executes_through_agent_runner():

    class ExecutionController:

        def __init__(self):

            self.calls = []

        def execute_tool(
            self,
            tool_name,
            permission_type,
            level,
            resource=None,
            **kwargs
        ):

            self.calls.append(
                {
                    "tool_name": tool_name,
                    "arguments": kwargs
                }
            )

            return {
                "success": True,
                "result": (
                    f"Executed {tool_name}"
                ),
                "error": None
            }

    agent = create_agent()

    task = agent.create_plan(
        "Calculate 25 * 4 and then calculate 100 + 50."
    )

    controller = ExecutionController()

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

    assert len(
        controller.calls
    ) == len(task.steps)

    assert len(
        controller.calls
    ) >= 2

    assert all(
        call["tool_name"]
        == "calculator"
        for call in controller.calls
    )

    assert all(
        step.status == "success"
        for step in task.steps
    )