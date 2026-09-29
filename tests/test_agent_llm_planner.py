from agent.llm_planner import AgentLLMPlanner


class MockProvider:

    def __init__(self):

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

        return "PLAN GENERATED"


def test_llm_planner_requires_provider():

    try:

        AgentLLMPlanner(None)

        assert False

    except ValueError as error:

        assert str(error) == (
            "AI provider cannot be None."
        )


def test_llm_planner_generates_plan():

    provider = MockProvider()

    planner = AgentLLMPlanner(
        provider
    )

    result = planner.generate_plan(
        "Calculate 25 * 4"
    )

    assert result == "PLAN GENERATED"

    assert len(provider.calls) == 1

    prompt = provider.calls[0][
        "prompt"
    ]

    assert (
        "Calculate 25 * 4"
        in prompt
    )

    assert (
        "Do not execute tools."
        in prompt
    )

    assert (
        "Only propose operations"
        in prompt
    )


def test_llm_planner_requires_json():

    provider = MockProvider()

    planner = AgentLLMPlanner(
        provider
    )

    planner.generate_plan(
        "Calculate 25 * 4"
    )

    prompt = provider.calls[0][
        "prompt"
    ]

    assert (
        "Return ONLY valid JSON."
        in prompt
    )

    assert (
        "Do not use Markdown."
        in prompt
    )

    assert (
        "Do not use code fences."
        in prompt
    )

    assert (
        '"steps"'
        in prompt
    )

    assert (
        '"tool"'
        in prompt
    )

    assert (
        '"arguments"'
        in prompt
    )

    assert (
        provider.calls[0]["format"]
        == "json"
    )


def test_llm_planner_passes_context():

    provider = MockProvider()

    planner = AgentLLMPlanner(
        provider
    )

    context = (
        "User previously created "
        "a calculator project."
    )

    planner.generate_plan(
        "Continue the project.",
        context=context
    )

    assert len(provider.calls) == 1

    assert provider.calls[0][
        "context"
    ] == context

    assert provider.calls[0][
        "format"
    ] == "json"


def test_llm_planner_rejects_none_request():

    provider = MockProvider()

    planner = AgentLLMPlanner(
        provider
    )

    try:

        planner.generate_plan(
            None
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent request cannot be empty."
        )


def test_llm_planner_rejects_empty_request():

    provider = MockProvider()

    planner = AgentLLMPlanner(
        provider
    )

    try:

        planner.generate_plan(
            "   "
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent request cannot be empty."
        )