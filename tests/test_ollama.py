import json

from brain.ollama import OllamaProvider
from brain.brain import SaraBrain


def test_ollama_health_check():

    provider = OllamaProvider(
        model="qwen2.5:3b"
    )

    assert provider.health_check() is True


def test_ollama_generate():

    provider = OllamaProvider(
        model="qwen2.5:3b",
        timeout=120
    )

    response = provider.generate(
        "Reply with exactly: SARA TEST PASSED"
    )

    assert isinstance(response, str)

    assert response.strip()

    assert "SARA TEST PASSED" in response.upper()


def test_ollama_generate_json():

    provider = OllamaProvider(
        model="qwen2.5:3b",
        timeout=120
    )

    response = provider.generate(
        (
            "Create a plan for: Calculate 25 * 4 "
            "using the calculator tool. "
            "Return an object with a steps array "
            "containing one step with tool calculator "
            "and arguments containing expression 25 * 4."
        ),
        format="json"
    )

    assert isinstance(response, str)

    assert response.strip()

    plan = json.loads(
        response
    )

    assert isinstance(
        plan,
        dict
    )

    assert "steps" in plan

    assert isinstance(
        plan["steps"],
        list
    )

    assert len(
        plan["steps"]
    ) == 1

    step = plan["steps"][0]

    assert step["tool"] == (
        "calculator"
    )

    assert step["arguments"][
        "expression"
    ] == "25 * 4"


def test_sara_brain_with_ollama():

    provider = OllamaProvider(
        model="qwen2.5:3b",
        timeout=120
    )

    brain = SaraBrain(
        provider=provider
    )

    result = brain.initialize()

    assert result is True

    assert brain.available is True

    response = brain.think(
        "Reply with exactly: BRAIN TEST PASSED"
    )

    assert isinstance(response, str)

    assert response.strip()

    assert "BRAIN TEST PASSED" in response.upper()