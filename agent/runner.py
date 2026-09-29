from agent.executor import AgentExecutor
from agent.recovery import AgentRecovery
from agent.reporter import AgentReporter
from agent.task import AgentTask
from agent.verifier import AgentVerifier


class AgentRunner:

    def __init__(
        self,
        controller,
        recovery=None,
        verifier=None,
        reporter=None
    ):

        if controller is None:

            raise ValueError(
                "Controller cannot be None."
            )

        self.executor = AgentExecutor(
            controller
        )

        self.recovery = (
            recovery
            if recovery is not None
            else AgentRecovery()
        )

        self.verifier = (
            verifier
            if verifier is not None
            else AgentVerifier()
        )

        self.reporter = (
            reporter
            if reporter is not None
            else AgentReporter()
        )

    def _resolve_step_arguments(
        self,
        step,
        previous_result
    ):

        if previous_result is None:

            return dict(
                step.arguments
            )

        resolved_arguments = {}

        for key, value in step.arguments.items():

            if isinstance(value, str):

                value = value.replace(
                    "[result of previous step]",
                    str(previous_result)
                )

                value = value.replace(
                    "result",
                    str(previous_result)
                )

            resolved_arguments[key] = value

        return resolved_arguments

    def run(
        self,
        task,
        permission_type,
        level
    ):

        if not isinstance(
            task,
            AgentTask
        ):

            raise ValueError(
                "Task must be an AgentTask."
            )

        task.status = "running"

        while (
            task.current_step
            < len(task.steps)
        ):

            step = task.steps[
                task.current_step
            ]

            previous_result = None

            if task.current_step > 0:

                previous_step = task.steps[
                    task.current_step - 1
                ]

                previous_result = (
                    previous_step.result
                )

            original_arguments = step.arguments

            step.arguments = (
                self._resolve_step_arguments(
                    step,
                    previous_result
                )
            )

            result = self.executor.execute_step(
                step=step,
                permission_type=permission_type,
                level=level
            )

            step.arguments = original_arguments

            if not result.get(
                "success"
            ):

                error = result.get(
                    "error"
                )

                if self.recovery.can_retry(
                    step,
                    error
                ):

                    continue

                task.status = "failed"

                task.error = error

                return task

            task.current_step += 1

        task.status = "completed"

        task.result = (
            task.steps[-1].result
            if task.steps
            else None
        )

        verified = self.verifier.verify(
            task
        )

        if not verified:

            task.status = "failed"

            task.error = (
                "Task verification failed."
            )

            return task

        task.report = self.reporter.report(
            task
        )

        return task