from agent.task import AgentTask
from agent.step import AgentStep


def test_agent_task_defaults():

    task = AgentTask(
        request="Test task"
    )

    assert task.request == "Test task"

    assert task.status == "pending"

    assert task.steps == []

    assert task.current_step == 0

    assert task.result is None

    assert task.error is None


def test_agent_task_accepts_steps():

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        }
    )

    task = AgentTask(
        request="Calculate 2 + 2",
        steps=[step]
    )

    assert len(task.steps) == 1

    assert task.steps[0] is step


def test_agent_step_defaults():

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        }
    )

    assert step.tool_name == "calculator"

    assert step.arguments == {
        "expression": "2 + 2"
    }

    assert step.status == "pending"

    assert step.result is None

    assert step.error is None

    assert step.attempts == 0


def test_agent_step_accepts_result():

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        },
        status="success",
        result=4,
        attempts=1
    )

    assert step.status == "success"

    assert step.result == 4

    assert step.attempts == 1