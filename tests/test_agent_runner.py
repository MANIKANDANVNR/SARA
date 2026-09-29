from agent.runner import AgentRunner
from agent.step import AgentStep
from agent.task import AgentTask

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
            "result": f"Executed {tool_name}",
            "error": None
        }


class FailingController:

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
            tool_name
        )

        return {
            "success": False,
            "result": None,
            "error": "Execution failed."
        }


class PartialFailingController:

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
            tool_name
        )

        if tool_name == "file_write":

            return {
                "success": False,
                "result": None,
                "error": "File write failed."
            }

        return {
            "success": True,
            "result": f"Executed {tool_name}",
            "error": None
        }


class RetryThenSuccessController:

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
            tool_name
        )

        if len(self.calls) == 1:

            return {
                "success": False,
                "result": None,
                "error": "Execution failed."
            }

        return {
            "success": True,
            "result": f"Executed {tool_name}",
            "error": None
        }


class PermissionDeniedController:

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
            tool_name
        )

        return {
            "success": False,
            "result": None,
            "error": "Permission denied."
        }


class MockVerifier:

    def __init__(
        self,
        result=True
    ):

        self.result = result

        self.calls = []

    def verify(
        self,
        task
    ):

        self.calls.append(
            task
        )

        return self.result


class MockReporter:

    def __init__(self):

        self.calls = []

    def report(
        self,
        task
    ):

        self.calls.append(
            task
        )

        return "Final report."


def test_runner_requires_controller():

    try:

        AgentRunner(
            None
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Controller cannot be None."
        )


def test_runner_requires_task():

    controller = MockController()

    runner = AgentRunner(
        controller
    )

    try:

        runner.run(
            task=None,
            permission_type=None,
            level=None
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Task must be an AgentTask."
        )


def test_runner_executes_single_step():

    controller = MockController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Test request"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == 1

    assert result.result == (
        "Executed calculator"
    )

    assert result.report == (
        "Task completed successfully "
        "with 1 step(s)."
    )

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == (
        "Executed calculator"
    )

    assert task.steps[0].error is None

    assert task.steps[0].attempts == 1

    assert len(
        controller.calls
    ) == 1

    assert controller.calls[0][
        "tool_name"
    ] == "calculator"


def test_runner_executes_multiple_steps():

    controller = MockController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Multiple steps"
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
            tool_name="file_write",
            arguments={
                "path": "result.txt",
                "content": "15"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == 2

    assert result.result == (
        "Executed file_write"
    )

    assert result.report == (
        "Task completed successfully "
        "with 2 step(s)."
    )

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == (
        "Executed calculator"
    )

    assert task.steps[1].status == (
        "success"
    )

    assert task.steps[1].result == (
        "Executed file_write"
    )

    assert len(
        controller.calls
    ) == 2

    assert (
        controller.calls[0][
            "tool_name"
        ]
        == "calculator"
    )

    assert (
        controller.calls[1][
            "tool_name"
        ]
        == "file_write"
    )


def test_runner_retries_retryable_failure_until_limit():

    controller = FailingController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Retrying task"
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

    assert result.status == (
        "failed"
    )

    assert result.error == (
        "Execution failed."
    )

    assert result.current_step == 0

    assert task.steps[0].status == (
        "failed"
    )

    assert task.steps[0].attempts == 3

    assert len(
        controller.calls
    ) == 3


def test_runner_retries_then_succeeds():

    controller = RetryThenSuccessController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Retry then succeed"
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

    assert result.status == (
        "completed"
    )

    assert result.current_step == 1

    assert result.result == (
        "Executed calculator"
    )

    assert result.report == (
        "Task completed successfully "
        "with 1 step(s)."
    )

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].attempts == 2

    assert task.steps[0].error is None

    assert controller.calls == [
        "calculator",
        "calculator"
    ]


def test_runner_does_not_retry_permission_failure():

    controller = PermissionDeniedController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Permission failure"
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

    assert result.status == (
        "failed"
    )

    assert result.error == (
        "Permission denied."
    )

    assert result.current_step == 0

    assert task.steps[0].attempts == 1

    assert len(
        controller.calls
    ) == 1


def test_runner_preserves_previous_results_after_failure():

    controller = PartialFailingController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Partial failure"
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
            tool_name="file_write",
            arguments={
                "path": "result.txt",
                "content": "15"
            }
        )
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
        "File write failed."
    )

    assert task.steps[0].status == (
        "success"
    )

    assert task.steps[0].result == (
        "Executed calculator"
    )

    assert task.steps[0].error is None

    assert task.steps[1].status == (
        "failed"
    )

    assert task.steps[1].result is None

    assert task.steps[1].error == (
        "File write failed."
    )

    assert task.steps[1].attempts == 1

    assert controller.calls == [
        "calculator",
        "file_write"
    ]


def test_runner_uses_trusted_permission_information():

    controller = MockController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Permission test"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "2 + 2"
            }
        )
    )

    permission_type = "TEST_PERMISSION"
    level = "TEST_LEVEL"

    runner.run(
        task=task,
        permission_type=permission_type,
        level=level
    )

    assert controller.calls[0][
        "permission_type"
    ] == PermissionType.CALCULATOR

    assert controller.calls[0][
        "level"
    ] == PermissionLevel.LOW


def test_runner_uses_verifier_after_execution():

    controller = MockController()

    verifier = MockVerifier(
        result=True
    )

    runner = AgentRunner(
        controller=controller,
        verifier=verifier
    )

    task = AgentTask(
        request="Verified task"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.result == (
        "Executed calculator"
    )

    assert result.report == (
        "Task completed successfully "
        "with 1 step(s)."
    )

    assert len(
        verifier.calls
    ) == 1

    assert verifier.calls[0] is task


def test_runner_fails_when_verification_fails():

    controller = MockController()

    verifier = MockVerifier(
        result=False
    )

    runner = AgentRunner(
        controller=controller,
        verifier=verifier
    )

    task = AgentTask(
        request="Unverified task"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
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

    assert result.result == (
        "Executed calculator"
    )

    assert result.report is None

    assert len(
        verifier.calls
    ) == 1

    assert verifier.calls[0] is task


def test_runner_accepts_custom_reporter():

    controller = MockController()

    reporter = MockReporter()

    runner = AgentRunner(
        controller=controller,
        reporter=reporter
    )

    task = AgentTask(
        request="Custom report"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.result == (
        "Executed calculator"
    )

    assert result.report == (
        "Final report."
    )

    assert len(
        reporter.calls
    ) == 1

    assert reporter.calls[0] is task


def test_runner_reports_only_after_verification():

    controller = MockController()

    verifier = MockVerifier(
        result=False
    )

    reporter = MockReporter()

    runner = AgentRunner(
        controller=controller,
        verifier=verifier,
        reporter=reporter
    )

    task = AgentTask(
        request="Verification before report"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            }
        )
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

    assert result.result == (
        "Executed calculator"
    )

    assert result.report is None

    assert len(
        verifier.calls
    ) == 1

    assert len(
        reporter.calls
    ) == 0

def test_runner_resolves_previous_step_result():

    controller = MockController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Sequential calculation"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "157 * 83"
            }
        )
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "result / 7"
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == 2

    assert result.result == (
        "Executed calculator"
    )

    assert task.steps[0].result == (
        "Executed calculator"
    )

    assert task.steps[1].result == (
        "Executed calculator"
    )

    assert task.steps[1].arguments[
        "expression"
    ] == "result / 7"

    assert len(
        controller.calls
    ) == 2

    assert controller.calls[0][
        "arguments"
    ]["expression"] == "157 * 83"

    assert controller.calls[1][
        "arguments"
    ]["expression"] == (
        "Executed calculator / 7"
    )


def test_runner_resolves_previous_step_result_placeholder():

    controller = MockController()

    runner = AgentRunner(
        controller
    )

    task = AgentTask(
        request="Previous result placeholder"
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
                "expression": (
                    "[result of previous step] * 2"
                )
            }
        )
    )

    result = runner.run(
        task=task,
        permission_type=None,
        level=None
    )

    assert result.status == (
        "completed"
    )

    assert result.current_step == 2

    assert controller.calls[1][
        "arguments"
    ]["expression"] == (
        "Executed calculator * 2"
    )

    assert task.steps[1].arguments[
        "expression"
    ] == (
        "[result of previous step] * 2"
    )