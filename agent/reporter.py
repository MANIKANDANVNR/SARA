from agent.task import AgentTask


class AgentReporter:

    def report(
        self,
        task
    ):

        if not isinstance(
            task,
            AgentTask
        ):

            raise ValueError(
                "Task must be an AgentTask."
            )

        if task.status == "completed":

            if not task.steps:

                return (
                    "Task completed successfully."
                )

            return (
                f"Task completed successfully "
                f"with {len(task.steps)} "
                f"step(s)."
            )

        if task.status == "failed":

            if task.error:

                return (
                    "Task failed: "
                    f"{task.error}"
                )

            return "Task failed."

        if task.status == "running":

            return "Task is still running."

        return (
            f"Task status: {task.status}."
        )