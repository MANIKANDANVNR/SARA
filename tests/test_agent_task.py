from agent.task import AgentTask


def test_agent_task_has_empty_report_by_default():

    task = AgentTask(
        request="Test request"
    )

    assert task.report is None


def test_agent_task_can_store_report():

    task = AgentTask(
        request="Test request"
    )

    task.report = (
        "Task completed successfully."
    )

    assert task.report == (
        "Task completed successfully."
    )


def test_agent_task_report_is_independent_from_result():

    task = AgentTask(
        request="Test request",
        result="Actual execution result"
    )

    task.report = (
        "Task completed successfully."
    )

    assert task.result == (
        "Actual execution result"
    )

    assert task.report == (
        "Task completed successfully."
    )