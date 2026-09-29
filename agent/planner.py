from agent.step import AgentStep
from agent.task import AgentTask


class AgentPlanner:

    def plan(self, request):

        if request is None:

            raise ValueError(
                "Agent request cannot be empty."
            )

        request = str(
            request
        ).strip()

        if not request:

            raise ValueError(
                "Agent request cannot be empty."
            )

        return AgentTask(
            request=request,
            steps=[]
        )

    def add_step(
        self,
        task,
        tool_name,
        arguments
    ):

        if not isinstance(
            task,
            AgentTask
        ):

            raise ValueError(
                "Task must be an AgentTask."
            )

        if not tool_name:

            raise ValueError(
                "Tool name cannot be empty."
            )

        tool_name = str(
            tool_name
        ).strip()

        if not tool_name:

            raise ValueError(
                "Tool name cannot be empty."
            )

        if arguments is None:

            arguments = {}

        step = AgentStep(
            tool_name=tool_name.lower(),
            arguments=dict(
                arguments
            )
        )

        task.steps.append(
            step
        )

        return step