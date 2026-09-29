from agent.reporter import AgentReporter
from agent.step import AgentStep
from agent.task import AgentTask


def create_reporter():
    return AgentReporter()


def test_reporter_requires_agent_task():
    reporter = create_reporter()

    try:
        reporter.report(None)
        assert False
    except ValueError as error:
        assert str(error) == (
            "Task must be an AgentTask."
        )


def test_report_completed_task():
    reporter = create_reporter()

    task = AgentTask(
        request="Calculate 2 + 2",
        status="completed",
        current_step=1,
        steps=[
            AgentStep(
                tool_name="calculator",
                arguments={
                    "expression": "2 + 2"
                },
                status="success",
                result=4
            )
        ],
        result=4
    )

    result = reporter.report(task)

    assert result == (
        "Task completed successfully "
        "with 1 step(s)."
    )


def test_report_completed_task_without_steps():
    reporter = create_reporter()

    task = AgentTask(
        request="Do nothing",
        status="completed",
        current_step=0,
        steps=[]
    )

    result = reporter.report(task)

    assert result == (
        "Task completed successfully."
    )


def test_report_failed_task_with_error():
    reporter = create_reporter()

    task = AgentTask(
        request="Write a file",
        status="failed",
        error="Permission denied."
    )

    result = reporter.report(task)

    assert result == (
        "Task failed: Permission denied."
    )


def test_report_failed_task_without_error():
    reporter = create_reporter()

    task = AgentTask(
        request="Write a file",
        status="failed"
    )

    result = reporter.report(task)

    assert result == "Task failed."


def test_report_running_task():
    reporter = create_reporter()

    task = AgentTask(
        request="Calculate something",
        status="running"
    )

    result = reporter.report(task)

    assert result == "Task is still running."


def test_report_pending_task():
    reporter = create_reporter()

    task = AgentTask(
        request="Calculate something",
        status="pending"
    )

    result = reporter.report(task)

    assert result == "Task status: pending."


def test_report_unknown_status():
    reporter = create_reporter()

    task = AgentTask(
        request="Calculate something",
        status="paused"
    )

    result = reporter.report(task)

    assert result == "Task status: paused."


def test_report_completed_task_with_multiple_steps():
    reporter = create_reporter()

    task = AgentTask(
        request="Calculate and save result",
        status="completed",
        current_step=2,
        steps=[
            AgentStep(
                tool_name="calculator",
                arguments={
                    "expression": "2 + 2"
                },
                status="success",
                result=4
            ),
            AgentStep(
                tool_name="file_write",
                arguments={
                    "path": "result.txt",
                    "content": "4"
                },
                status="success",
                result={
                    "path": "result.txt",
                    "bytes_written": 1
                }
            )
        ],
        result={
            "path": "result.txt",
            "bytes_written": 1
        }
    )

    result = reporter.report(task)

    assert result == (
        "Task completed successfully "
        "with 2 step(s)."
    )


def test_reporter_does_not_modify_task():
    reporter = create_reporter()

    task = AgentTask(
        request="Calculate 2 + 2",
        status="completed",
        current_step=1,
        steps=[
            AgentStep(
                tool_name="calculator",
                arguments={
                    "expression": "2 + 2"
                },
                status="success",
                result=4
            )
        ],
        result=4
    )

    original_status = task.status
    original_current_step = task.current_step
    original_result = task.result

    reporter.report(task)

    assert task.status == original_status
    assert task.current_step == original_current_step
    assert task.result == original_result