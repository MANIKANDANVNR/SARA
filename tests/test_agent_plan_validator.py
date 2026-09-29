from agent.plan_validator import AgentPlanValidator

from tools.calculator import CalculatorTool
from tools.file_write_tool import FileWriteTool
from tools.tool_registry import ToolRegistry


class MockToolRegistry:

    def __init__(self):

        self.tools = {
            "calculator",
            "file_write"
        }

    def exists(
        self,
        name
    ):

        return name in self.tools


def test_validator_requires_tool_registry():

    try:

        AgentPlanValidator(None)

        assert False

    except ValueError as error:

        assert str(error) == (
            "Tool registry cannot be None."
        )


def test_validator_creates_task():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "calculator",
                "arguments": {
                    "expression": "25 * 4"
                }
            }
        ]
    }

    task = validator.validate(
        "Calculate 25 * 4",
        plan
    )

    assert task.request == (
        "Calculate 25 * 4"
    )

    assert len(task.steps) == 1

    assert task.steps[0].tool_name == (
        "calculator"
    )

    assert task.steps[0].arguments == {
        "expression": "25 * 4"
    }


def test_validator_accepts_multiple_steps():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "calculator",
                "arguments": {
                    "expression": "10 + 5"
                }
            },
            {
                "tool": "file_write",
                "arguments": {
                    "path": "result.txt",
                    "content": "15"
                }
            }
        ]
    }

    task = validator.validate(
        "Calculate 10 + 5 and save the result.",
        plan
    )

    assert len(task.steps) == 2

    assert (
        task.steps[0].tool_name
        == "calculator"
    )

    assert (
        task.steps[1].tool_name
        == "file_write"
    )


def test_validator_rejects_invalid_request():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    try:

        validator.validate(
            None,
            {}
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent request cannot be empty."
        )


def test_validator_rejects_empty_request():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    try:

        validator.validate(
            "   ",
            {}
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent request cannot be empty."
        )


def test_validator_rejects_non_dictionary_plan():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    try:

        validator.validate(
            "Test request",
            []
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan must be a dictionary."
        )


def test_validator_rejects_missing_steps():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    try:

        validator.validate(
            "Test request",
            {}
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan steps must be a list."
        )


def test_validator_rejects_invalid_step():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            "invalid step"
        ]
    }

    try:

        validator.validate(
            "Test request",
            plan
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Each agent step must be a dictionary."
        )


def test_validator_rejects_missing_tool():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "arguments": {}
            }
        ]
    }

    try:

        validator.validate(
            "Test request",
            plan
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent step tool is required."
        )


def test_validator_rejects_unknown_tool():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "delete_everything",
                "arguments": {}
            }
        ]
    }

    try:

        validator.validate(
            "Test request",
            plan
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Unknown agent tool: "
            "delete_everything"
        )


def test_validator_rejects_invalid_arguments():

    registry = MockToolRegistry()

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "calculator",
                "arguments": "invalid"
            }
        ]
    }

    try:

        validator.validate(
            "Test request",
            plan
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent step arguments "
            "must be a dictionary."
        )

def test_validator_rejects_missing_required_calculator_argument():

    registry = ToolRegistry()

    registry.register(
        "calculator",
        CalculatorTool()
    )

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "calculator",
                "arguments": {}
            }
        ]
    }

    try:

        validator.validate(
            "Calculate 157 * 83",
            plan
        )

        assert False

    except ValueError as error:

        assert (
            "Invalid arguments for agent tool "
            "'calculator'"
            in str(error)
        )


def test_validator_accepts_valid_calculator_argument():

    registry = ToolRegistry()

    registry.register(
        "calculator",
        CalculatorTool()
    )

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "calculator",
                "arguments": {
                    "expression": "157 * 83"
                }
            }
        ]
    }

    task = validator.validate(
        "Calculate 157 * 83",
        plan
    )

    assert len(task.steps) == 1

    assert task.steps[0].arguments == {
        "expression": "157 * 83"
    }


def test_validator_rejects_missing_file_write_argument():

    registry = ToolRegistry()

    registry.register(
        "file_write",
        FileWriteTool()
    )

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "file_write",
                "arguments": {
                    "path": "result.txt"
                }
            }
        ]
    }

    try:

        validator.validate(
            "Write the result to a file.",
            plan
        )

        assert False

    except ValueError as error:

        assert (
            "Invalid arguments for agent tool "
            "'file_write'"
            in str(error)
        )


def test_validator_accepts_optional_file_write_encoding():

    registry = ToolRegistry()

    registry.register(
        "file_write",
        FileWriteTool()
    )

    validator = AgentPlanValidator(
        registry
    )

    plan = {
        "steps": [
            {
                "tool": "file_write",
                "arguments": {
                    "path": "result.txt",
                    "content": "15"
                }
            }
        ]
    }

    task = validator.validate(
        "Write 15 to result.txt.",
        plan
    )

    assert len(task.steps) == 1

    assert task.steps[0].arguments == {
        "path": "result.txt",
        "content": "15"
    }