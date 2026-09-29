from agent.agent import SaraAgent


class MockProvider:

    def __init__(self, response):

        self.response = response

        self.calls = []

    def generate(
        self,
        prompt,
        context=None,
        format=None
    ):

        self.calls.append(
            {
                "prompt": prompt,
                "context": context,
                "format": format
            }
        )

        return self.response


class MockToolRegistry:

    def __init__(self):

        self.tools = {
            "calculator",
            "file_write"
        }

    def exists(
        self,
        name
    ):

        return name in self.tools

    def get_definitions(self):

        return [
            {
                "name": "calculator",
                "description": (
                    "Safely evaluates basic "
                    "mathematical expressions."
                )
            },
            {
                "name": "file_write",
                "description": (
                    "Safely writes text content "
                    "to a local filesystem file."
                )
            }
        ]


def test_agent_requires_provider():

    registry = MockToolRegistry()

    try:

        SaraAgent(
            None,
            registry
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "AI provider cannot be None."
        )


def test_agent_requires_tool_registry():

    provider = MockProvider(
        '{"steps": []}'
    )

    try:

        SaraAgent(
            provider,
            None
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Tool registry cannot be None."
        )


def test_agent_creates_valid_plan():

    response = """
    {
        "steps": [
            {
                "tool": "calculator",
                "arguments": {
                    "expression": "25 * 4"
                }
            }
        ]
    }
    """

    provider = MockProvider(
        response
    )

    registry = MockToolRegistry()

    agent = SaraAgent(
        provider,
        registry
    )

    task = agent.create_plan(
        "Calculate 25 * 4"
    )

    assert task.request == (
        "Calculate 25 * 4"
    )

    assert len(
        task.steps
    ) == 1

    assert task.steps[0].tool_name == (
        "calculator"
    )

    assert task.steps[0].arguments == {
        "expression": "25 * 4"
    }

    assert len(
        provider.calls
    ) == 1

    assert (
        provider.calls[0]["format"]
        == "json"
    )

    assert (
        "calculator"
        in provider.calls[0]["prompt"]
    )


def test_agent_passes_context():

    response = """
    {
        "steps": []
    }
    """

    provider = MockProvider(
        response
    )

    registry = MockToolRegistry()

    agent = SaraAgent(
        provider,
        registry
    )

    context = (
        "User previously created "
        "a calculator project."
    )

    agent.create_plan(
        "Continue the project.",
        context=context
    )

    assert len(
        provider.calls
    ) == 1

    assert provider.calls[0][
        "context"
    ] == context

    assert provider.calls[0][
        "format"
    ] == "json"


def test_agent_rejects_unknown_tool():

    response = """
    {
        "steps": [
            {
                "tool": "delete_everything",
                "arguments": {}
            }
        ]
    }
    """

    provider = MockProvider(
        response
    )

    registry = MockToolRegistry()

    agent = SaraAgent(
        provider,
        registry
    )

    try:

        agent.create_plan(
            "Delete everything."
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Unknown agent tool: "
            "delete_everything"
        )


def test_agent_rejects_invalid_llm_response():

    provider = MockProvider(
        "I will calculate that for you."
    )

    registry = MockToolRegistry()

    agent = SaraAgent(
        provider,
        registry
    )

    try:

        agent.create_plan(
            "Calculate 25 * 4"
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response must "
            "contain valid JSON."
        )