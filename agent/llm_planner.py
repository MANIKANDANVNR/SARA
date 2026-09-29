class AgentLLMPlanner:

    def __init__(self, provider):

        if provider is None:

            raise ValueError(
                "AI provider cannot be None."
            )

        self.provider = provider

    def generate_plan(
        self,
        request,
        context=None,
        tool_definitions=None
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

        if tool_definitions is None:

            tool_definitions = []

        tool_information = []

        for definition in tool_definitions:

            if not isinstance(
                definition,
                dict
            ):

                continue

            name = definition.get(
                "name"
            )

            description = definition.get(
                "description",
                ""
            )

            if not name:

                continue

            tool_information.append(
                f"- {name}: {description}"
            )

        available_tools = (
            "\n".join(
                tool_information
            )
            if tool_information
            else "No tools are currently available."
        )

        prompt = (
            "You are the planning component of "
            "SARA, a secure personal AI assistant.\n\n"

            "Your job is to analyze the user's request "
            "and propose a sequence of tool operations.\n\n"

            "Return ONLY valid JSON.\n"
            "Do not use Markdown.\n"
            "Do not use code fences.\n"
            "Do not include explanations.\n"
            "Do not execute tools.\n"
            "Do not claim that tools were executed.\n\n"

                        "IMPORTANT TOOL RULES:\n"
            "Only use tools from the available tools list.\n"
            "The tool name in every step MUST exactly match "
            "one of the available tool names.\n"
            "Do not invent, rename, combine, or substitute "
            "tool names.\n\n"
            "IMPORTANT MULTI-STEP RULES:\n"
            "When the user requests multiple operations, "
            "create ONE step for EACH operation in the exact "
            "order requested by the user.\n"
            "Never combine multiple requested operations into "
            "one tool call.\n"
            "For sequential calculations, the result of one "
            "step must be available to the next step.\n"
            "Do not use unresolved placeholders such as "
            "'[result of previous step]' when a later step "
            "depends on the previous result.\n"
            "Do not invent intermediate numeric results.\n"
            "Do not skip, reorder, or merge requested operations.\n\n"

            "AVAILABLE TOOLS:\n"
            f"{available_tools}\n\n"

            "The JSON must use exactly this general "
            "structure:\n\n"

            "{\n"
            '    "steps": [\n'
            "        {\n"
            '            "tool": "tool_name",\n'
            '            "arguments": {}\n'
            "        }\n"
            "    ]\n"
            "}\n\n"

            "Only propose operations that are necessary "
            "to complete the user's request.\n"
            "For calculator tasks involving sequential "
            "operations, preserve the user's operation order "
            "and create a separate calculator step for each "
            "operation.\n"
            "A later calculator step may reference the result "
            "of the immediately preceding step using the exact "
            "runtime reference: 'result'.\n\n"

            "USER REQUEST:\n"
            f"{request}"
        )

        return self.provider.generate(
            prompt=prompt,
            context=context,
            format="json"
        )