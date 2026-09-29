from brain.brain import SaraBrain
from brain.provider import AIProvider


class MockProvider(AIProvider):

    name = "mock"
    model = "test-model"

    def __init__(self):
        self.calls = []

    def health_check(self):
        return True

    def generate(self, prompt, context=None):
        self.calls.append({
            "prompt": prompt,
            "context": context
        })

        return f"Mock response to: {prompt}"


def test_brain_initially_unavailable():

    brain = SaraBrain()

    assert brain.available is False


def test_brain_initialization():

    provider = MockProvider()

    brain = SaraBrain(provider)

    result = brain.initialize()

    assert result is True
    assert brain.available is True


def test_brain_generation():

    provider = MockProvider()

    brain = SaraBrain(provider)

    brain.initialize()

    result = brain.think("Hello SARA")

    assert result == "Mock response to: Hello SARA"


def test_brain_uses_context():

    provider = MockProvider()

    brain = SaraBrain(provider)

    brain.initialize()

    result = brain.think(
        "What am I building?",
        context="User is building SARA."
    )

    assert "What am I building?" in result

    assert (
        provider.calls[0]["context"]
        == "User is building SARA."
    )


def test_brain_failure_without_provider():

    brain = SaraBrain()

    result = brain.think("Hello")

    assert "not available" in result


def test_brain_status():

    provider = MockProvider()

    brain = SaraBrain(provider)

    brain.initialize()

    status = brain.status()

    assert status["available"] is True
    assert status["provider"] == "mock"
    assert status["model"] == "test-model"


def test_brain_has_no_direct_tool_access():

    provider = MockProvider()

    brain = SaraBrain(provider)

    brain.initialize()

    assert not hasattr(
        brain,
        "execute_tool"
    )

    assert not hasattr(
        brain,
        "read_file"
    )

    assert not hasattr(
        brain,
        "access_internet"
    )

    assert not hasattr(
        brain,
        "execute_system_command"
    )