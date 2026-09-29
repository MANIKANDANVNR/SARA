from agent.planner import AgentPlanner
from agent.step import AgentStep
from agent.task import AgentTask


def test_planner_creates_task():

    planner = AgentPlanner()

    task = planner.plan(
        "Calculate 25 * 4"
    )

    assert isinstance(
        task,
        AgentTask
    )

    assert task.request == (
        "Calculate 25 * 4"
    )

    assert task.status == "pending"

    assert task.steps == []


def test_planner_rejects_none_request():

    planner = AgentPlanner()

    try:

        planner.plan(None)

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent request cannot be empty."
        )


def test_planner_rejects_empty_request():

    planner = AgentPlanner()

    try:

        planner.plan("   ")

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent request cannot be empty."
        )


def test_planner_adds_step():

    planner = AgentPlanner()

    task = planner.plan(
        "Calculate 25 * 4"
    )

    step = planner.add_step(
        task=task,
        tool_name="calculator",
        arguments={
            "expression": "25 * 4"
        }
    )

    assert isinstance(
        step,
        AgentStep
    )

    assert step.tool_name == (
        "calculator"
    )

    assert step.arguments == {
        "expression": "25 * 4"
    }

    assert len(task.steps) == 1

    assert task.steps[0] is step


def test_planner_normalizes_tool_name():

    planner = AgentPlanner()

    task = planner.plan(
        "Test"
    )

    step = planner.add_step(
        task=task,
        tool_name="  CALCULATOR  ",
        arguments={}
    )

    assert step.tool_name == (
        "calculator"
    )


def test_planner_accepts_none_arguments():

    planner = AgentPlanner()

    task = planner.plan(
        "Test"
    )

    step = planner.add_step(
        task=task,
        tool_name="calculator",
        arguments=None
    )

    assert step.arguments == {}


def test_planner_rejects_invalid_task():

    planner = AgentPlanner()

    try:

        planner.add_step(
            task=None,
            tool_name="calculator",
            arguments={}
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Task must be an AgentTask."
        )


def test_planner_rejects_empty_tool_name():

    planner = AgentPlanner()

    task = planner.plan(
        "Test"
    )

    try:

        planner.add_step(
            task=task,
            tool_name="   ",
            arguments={}
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Tool name cannot be empty."
        )