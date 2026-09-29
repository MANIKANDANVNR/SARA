from agent.step import AgentStep
from agent.security_policy import AgentSecurityPolicy


class AgentExecutor:

    def __init__(
        self,
        controller,
        security_policy=None
    ):

        if controller is None:

            raise ValueError(
                "Controller cannot be None."
            )

        self.controller = controller

        self.security_policy = (
            security_policy
            if security_policy is not None
            else AgentSecurityPolicy()
        )

    def execute_step(
        self,
        step,
        permission_type=None,
        level=None,
        resource=None
    ):

        if not isinstance(
            step,
            AgentStep
        ):

            raise ValueError(
                "Step must be an AgentStep."
            )

        if not step.tool_name:

            raise ValueError(
                "Agent step tool name cannot be empty."
            )

        if not isinstance(
                step.arguments,
                dict
        ):
            raise ValueError(
                "Agent step arguments must be a dictionary."
            )

        policy = self.security_policy.get_policy(
            step.tool_name
        )

        if policy is not None:

            permission_type = policy[
                "permission_type"
            ]

            level = policy[
                "level"
            ]

            resource = (
                self.security_policy.get_resource(
                    step.tool_name,
                    step.arguments
                )
            )

        elif (
            permission_type is None
            or level is None
        ):

            raise ValueError(
                "Security policy is unavailable "
                "for this agent tool."
            )

        step.status = "running"

        step.attempts += 1

        result = self.controller.execute_tool(
            tool_name=step.tool_name,
            permission_type=permission_type,
            level=level,
            resource=resource,
            **step.arguments
        )

        if result.get("success"):

            step.status = "success"

            step.result = result.get(
                "result"
            )

            step.error = None

        else:

            step.status = "failed"

            step.result = None

            step.error = result.get(
                "error"
            )

        return result