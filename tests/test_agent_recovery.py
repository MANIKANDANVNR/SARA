from agent.recovery import AgentRecovery
from agent.step import AgentStep


def test_recovery_marks_execution_failure_retryable():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Execution failed."
    ) is True


def test_recovery_marks_connection_failure_retryable():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Connection failed."
    ) is True


def test_recovery_marks_timeout_retryable():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Timeout."
    ) is True


def test_recovery_rejects_permission_failure():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Permission denied."
    ) is False


def test_recovery_rejects_unknown_tool():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Unknown tool."
    ) is False


def test_recovery_rejects_invalid_arguments():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Invalid arguments."
    ) is False


def test_recovery_rejects_empty_error():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        ""
    ) is False


def test_recovery_rejects_none_error():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        None
    ) is False


def test_recovery_rejects_unknown_error():

    recovery = AgentRecovery()

    assert recovery.is_retryable(
        "Something unexpected happened."
    ) is False


def test_recovery_default_max_attempts():

    recovery = AgentRecovery()

    assert recovery.max_attempts == 3


def test_recovery_accepts_custom_max_attempts():

    recovery = AgentRecovery(
        max_attempts=5
    )

    assert recovery.max_attempts == 5


def test_recovery_rejects_invalid_max_attempts_type():

    try:

        AgentRecovery(
            max_attempts="3"
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Maximum attempts must be an integer."
        )


def test_recovery_rejects_zero_max_attempts():

    try:

        AgentRecovery(
            max_attempts=0
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Maximum attempts must be at least 1."
        )


def test_recovery_can_retry_failed_step():

    recovery = AgentRecovery()

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        },
        attempts=1
    )

    assert recovery.can_retry(
        step,
        "Execution failed."
    ) is True


def test_recovery_cannot_retry_at_limit():

    recovery = AgentRecovery()

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        },
        attempts=3
    )

    assert recovery.can_retry(
        step,
        "Execution failed."
    ) is False


def test_recovery_cannot_retry_non_retryable_error():

    recovery = AgentRecovery()

    step = AgentStep(
        tool_name="calculator",
        arguments={
            "expression": "2 + 2"
        },
        attempts=1
    )

    assert recovery.can_retry(
        step,
        "Permission denied."
    ) is False


def test_recovery_cannot_retry_none_step():

    recovery = AgentRecovery()

    assert recovery.can_retry(
        None,
        "Execution failed."
    ) is False