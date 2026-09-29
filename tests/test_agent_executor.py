from agent.executor import AgentExecutor
from agent.step import AgentStep

from security.permission import (
    PermissionType,
    PermissionLevel
)


class MockController:

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
                "permission_type": permission_type,
                "level": level,
                "resource": resource,
                "arguments": kwargs
            }
        )

        return {
            "success": True,
            "result": 4,
            "error": None
        }


class FailingController:

    def execute_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        **kwargs
    ):

        return {
            "success": False,
            "result": None,
            "error": "Tool execution failed."
        }


def test_agent_executor_requires_controller():

    try:

        AgentExecutor(None)

        assert False

    except ValueError as error:

        assert str(error) == (
            "Controller cannot be None."
        )


def test_agent_executor_executes_step():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        }
    )

    result = executor.execute_step(
        step=step,
        permission_type="system",
        level="medium"
    )

    assert result["success"] is True

    assert step.status == "success"

    assert step.result == 4

    assert step.error is None

    assert step.attempts == 1

    assert len(controller.calls) == 1

    assert controller.calls[0][
        "tool_name"
    ] == "calculator"

    assert controller.calls[0][
        "arguments"
    ] == {
        "expression": "2 + 2"
    }


def test_agent_executor_records_failure():

    controller = FailingController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        }
    )

    result = executor.execute_step(
        step=step,
        permission_type="system",
        level="medium"
    )

    assert result["success"] is False

    assert step.status == "failed"

    assert step.result is None

    assert step.error == (
        "Tool execution failed."
    )

    assert step.attempts == 1


def test_agent_executor_rejects_invalid_step():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    try:

        executor.execute_step(
            step=None,
            permission_type="system",
            level="medium"
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Step must be an AgentStep."
        )


def test_agent_executor_rejects_empty_tool_name():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="",
        arguments={}
    )

    try:

        executor.execute_step(
            step=step,
            permission_type="system",
            level="medium"
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent step tool name cannot be empty."
        )


def test_agent_executor_uses_trusted_calculator_policy():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "25 * 4"
        }
    )

    result = executor.execute_step(
        step=step,
        permission_type="wrong_permission",
        level="wrong_level"
    )

    assert result["success"] is True

    assert controller.calls[0][
        "permission_type"
    ] == PermissionType.CALCULATOR

    assert controller.calls[0][
        "level"
    ] == PermissionLevel.LOW


def test_agent_executor_uses_trusted_file_write_policy():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="file_write",
        arguments={
            "path": "test.txt",
            "content": "hello"
        }
    )

    executor.execute_step(
        step=step,
        permission_type="wrong_permission",
        level="wrong_level"
    )

    assert controller.calls[0][
        "permission_type"
    ] == PermissionType.WRITE_FILE

    assert controller.calls[0][
        "level"
    ] == PermissionLevel.LOW

    assert controller.calls[0][
        "resource"
    ] == "test.txt"


def test_agent_executor_rejects_unknown_tool_without_security_policy():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="unknown_tool",
        arguments={}
    )

    try:

        executor.execute_step(
            step=step
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Security policy is unavailable "
            "for this agent tool."
        )

def test_agent_executor_ignores_caller_resource_for_file_write():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="file_write",
        arguments={
            "path": "approved.txt",
            "content": "hello"
        }
    )

    executor.execute_step(
        step=step,
        permission_type=PermissionType.WRITE_FILE,
        level=PermissionLevel.LOW,
        resource="attacker_supplied.txt"
    )

    assert controller.calls[0][
        "resource"
    ] == "approved.txt"


def test_agent_executor_rejects_caller_resource_when_policy_resource_missing():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="file_write",
        arguments={
            "content": "hello"
        }
    )

    executor.execute_step(
        step=step,
        permission_type=PermissionType.WRITE_FILE,
        level=PermissionLevel.LOW,
        resource="attacker_supplied.txt"
    )

    assert controller.calls[0][
        "resource"
    ] is None

def test_agent_executor_rejects_invalid_arguments():

    controller = MockController()

    executor = AgentExecutor(
        controller
    )

    step = AgentStep(
        tool_name="calculator",
        arguments=None
    )

    try:

        executor.execute_step(
            step=step,
            permission_type=PermissionType.CALCULATOR,
            level=PermissionLevel.LOW
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent step arguments must be a dictionary."
        )

    assert len(
        controller.calls
    ) == 0

