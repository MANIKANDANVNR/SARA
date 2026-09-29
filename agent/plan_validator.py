import inspect

from agent.planner import AgentPlanner
from agent.task import AgentTask


class AgentPlanValidator:

    def __init__(self, tool_registry):

        if tool_registry is None:

            raise ValueError(
                "Tool registry cannot be None."
            )

        self.tool_registry = tool_registry

        self.planner = AgentPlanner()

    def _validate_tool_arguments(
        self,
        tool_name,
        arguments
    ):

        get_tool = getattr(
            self.tool_registry,
            "get",
            None
        )

        if not callable(get_tool):

            return

        tool = get_tool(
            tool_name
        )

        if tool is None:

            return

        execute = getattr(
            tool,
            "execute",
            None
        )

        if not callable(execute):

            return

        try:

            signature = inspect.signature(
                execute
            )

            signature.bind(
                **arguments
            )

        except TypeError as error:

            raise ValueError(
                f"Invalid arguments for "
                f"agent tool '{tool_name}': "
                f"{error}"
            ) from error

    def validate(
        self,
        request,
        plan
    ):

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

        if not isinstance(
            plan,
            dict
        ):

            raise ValueError(
                "Agent plan must be a dictionary."
            )

        steps = plan.get(
            "steps"
        )

        if not isinstance(
            steps,
            list
        ):

            raise ValueError(
                "Agent plan steps must be a list."
            )

        task = self.planner.plan(
            request
        )

        for step_data in steps:

            if not isinstance(
                step_data,
                dict
            ):

                raise ValueError(
                    "Each agent step must be a dictionary."
                )

            tool_name = step_data.get(
                "tool"
            )

            arguments = step_data.get(
                "arguments",
                {}
            )

            if not tool_name:

                raise ValueError(
                    "Agent step tool is required."
                )

            tool_name = str(
                tool_name
            ).strip().lower()

            if not tool_name:

                raise ValueError(
                    "Agent step tool is required."
                )

            if not self.tool_registry.exists(
                tool_name
            ):

                raise ValueError(
                    f"Unknown agent tool: "
                    f"{tool_name}"
                )

            if not isinstance(
                arguments,
                dict
            ):

                raise ValueError(
                    "Agent step arguments "
                    "must be a dictionary."
                )

            self._validate_tool_arguments(
                tool_name,
                arguments
            )

            self.planner.add_step(
                task=task,
                tool_name=tool_name,
                arguments=arguments
            )

        return task