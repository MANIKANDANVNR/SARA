from agent.plan_parser import AgentPlanParser


def test_parser_accepts_valid_json_object():

    parser = AgentPlanParser()

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

    plan = parser.parse(
        response
    )

    assert isinstance(
        plan,
        dict
    )

    assert plan["steps"][0]["tool"] == (
        "calculator"
    )

    assert plan["steps"][0]["arguments"] == {
        "expression": "25 * 4"
    }


def test_parser_accepts_multiple_steps():

    parser = AgentPlanParser()

    response = """
    {
        "steps": [
            {
                "tool": "calculator",
                "arguments": {
                    "expression": "10 + 5"
                }
            },
            {
                "tool": "file_write",
                "arguments": {
                    "path": "result.txt",
                    "content": "15"
                }
            }
        ]
    }
    """

    plan = parser.parse(
        response
    )

    assert len(
        plan["steps"]
    ) == 2


def test_parser_rejects_none():

    parser = AgentPlanParser()

    try:

        parser.parse(
            None
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response cannot be empty."
        )


def test_parser_rejects_empty_response():

    parser = AgentPlanParser()

    try:

        parser.parse(
            "   "
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response cannot be empty."
        )


def test_parser_rejects_invalid_json():

    parser = AgentPlanParser()

    try:

        parser.parse(
            "This is not JSON."
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response must "
            "contain valid JSON."
        )


def test_parser_rejects_natural_language():

    parser = AgentPlanParser()

    response = (
        "Sure! I will calculate "
        "25 multiplied by 4."
    )

    try:

        parser.parse(
            response
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response must "
            "contain valid JSON."
        )


def test_parser_rejects_json_array():

    parser = AgentPlanParser()

    response = """
    [
        {
            "tool": "calculator",
            "arguments": {
                "expression": "25 * 4"
            }
        }
    ]
    """

    try:

        parser.parse(
            response
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response must "
            "be a JSON object."
        )


def test_parser_rejects_json_string():

    parser = AgentPlanParser()

    response = '"calculator"'

    try:

        parser.parse(
            response
        )

        assert False

    except ValueError as error:

        assert str(error) == (
            "Agent plan response must "
            "be a JSON object."
        )


def test_parser_preserves_extra_fields():

    parser = AgentPlanParser()

    response = """
    {
        "steps": [],
        "reason": "No tools required."
    }
    """

    plan = parser.parse(
        response
    )

    assert plan["steps"] == []

    assert plan["reason"] == (
        "No tools required."
    )