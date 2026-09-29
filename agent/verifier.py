from agent.task import AgentTask


class AgentVerifier:

    def verify(
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

        if task.status != "completed":

            return False

        if task.current_step != len(
            task.steps
        ):

            return False

        for step in task.steps:

            if step.status != "success":

                return False

            if step.error is not None:

                return False

        return True