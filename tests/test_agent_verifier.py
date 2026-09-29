from agent.step import AgentStep
from agent.task import AgentTask
from agent.verifier import AgentVerifier


def create_completed_task():

    task = AgentTask(
        request="Test task"
    )

    task.steps.append(
        AgentStep(
            tool_name="calculator",
            arguments={
                "expression": "25 * 4"
            },
            status="success",
            result=100,
            error=None,
            attempts=1
        )
    )

    task.current_step = 1

    task.status = "completed"

    task.result = 100

    return task


def test_verifier_requires_task():

    verifier = AgentVerifier()

    try:

        verifier.verify(
            None
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Task must be an AgentTask."
        )


def test_verifier_accepts_completed_task():

    verifier = AgentVerifier()

    task = create_completed_task()

    assert verifier.verify(
        task
    ) is True


def test_verifier_rejects_pending_task():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.status = "pending"

    assert verifier.verify(
        task
    ) is False


def test_verifier_rejects_running_task():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.status = "running"

    assert verifier.verify(
        task
    ) is False


def test_verifier_rejects_failed_task():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.status = "failed"

    assert verifier.verify(
        task
    ) is False


def test_verifier_rejects_incomplete_steps():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.current_step = 0

    assert verifier.verify(
        task
    ) is False


def test_verifier_rejects_failed_step():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.steps[0].status = "failed"

    assert verifier.verify(
        task
    ) is False


def test_verifier_rejects_step_with_error():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.steps[0].error = (
        "Execution failed."
    )

    assert verifier.verify(
        task
    ) is False


def test_verifier_rejects_multiple_steps_with_failure():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.steps.append(
        AgentStep(
            tool_name="file_write",
            arguments={
                "path": "result.txt",
                "content": "100"
            },
            status="failed",
            result=None,
            error="File write failed.",
            attempts=1
        )
    )

    task.current_step = 2

    assert verifier.verify(
        task
    ) is False


def test_verifier_accepts_multiple_successful_steps():

    verifier = AgentVerifier()

    task = create_completed_task()

    task.steps.append(
        AgentStep(
            tool_name="file_write",
            arguments={
                "path": "result.txt",
                "content": "100"
            },
            status="success",
            result="Executed file_write",
            error=None,
            attempts=1
        )
    )

    task.current_step = 2

    task.result = (
        "Executed file_write"
    )

    assert verifier.verify(
        task
    ) is True