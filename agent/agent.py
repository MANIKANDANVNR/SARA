from agent.llm_planner import AgentLLMPlanner
from agent.plan_parser import AgentPlanParser
from agent.plan_validator import AgentPlanValidator


class SaraAgent:

    def __init__(
        self,
        provider,
        tool_registry
    ):

        if provider is None:

            raise ValueError(
                "AI provider cannot be None."
            )

        if tool_registry is None:

            raise ValueError(
                "Tool registry cannot be None."
            )

        self.tool_registry = tool_registry

        self.llm_planner = AgentLLMPlanner(
            provider
        )

        self.plan_parser = AgentPlanParser()

        self.plan_validator = AgentPlanValidator(
            tool_registry
        )

    def create_plan(
        self,
        request,
        context=None
    ):

        tool_definitions = (
            self.tool_registry.get_definitions()
        )

        response = (
            self.llm_planner.generate_plan(
                request=request,
                context=context,
                tool_definitions=tool_definitions
            )
        )

        plan = self.plan_parser.parse(
            response
        )

        task = self.plan_validator.validate(
            request=request,
            plan=plan
        )

        return task