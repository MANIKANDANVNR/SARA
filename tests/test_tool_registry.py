import pytest

from tools.tool_registry import ToolRegistry


class MockTool:

    description = "Mock tool"


def create_registry():

    return ToolRegistry()


def test_registry_starts_empty():

    registry = create_registry()

    assert registry.count() == 0
    assert registry.list_tools() == []


def test_register_tool():

    registry = create_registry()
    tool = MockTool()

    result = registry.register(
        "calculator",
        tool
    )

    assert result is True
    assert registry.count() == 1
    assert registry.exists("calculator")


def test_get_registered_tool():

    registry = create_registry()
    tool = MockTool()

    registry.register(
        "calculator",
        tool
    )

    assert registry.get("calculator") is tool


def test_register_duplicate_tool_fails():

    registry = create_registry()
    tool = MockTool()

    registry.register(
        "calculator",
        tool
    )

    with pytest.raises(ValueError):

        registry.register(
            "calculator",
            tool
        )


def test_register_empty_name_fails():

    registry = create_registry()
    tool = MockTool()

    with pytest.raises(ValueError):

        registry.register(
            "",
            tool
        )


def test_register_none_tool_fails():

    registry = create_registry()

    with pytest.raises(ValueError):

        registry.register(
            "calculator",
            None
        )


def test_tool_names_are_normalized():

    registry = create_registry()
    tool = MockTool()

    registry.register(
        "  Calculator  ",
        tool
    )

    assert registry.exists("calculator")
    assert registry.get("CALCULATOR") is tool


def test_get_unknown_tool_returns_none():

    registry = create_registry()

    assert registry.get("unknown") is None
    assert registry.exists("unknown") is False


def test_unregister_tool():

    registry = create_registry()
    tool = MockTool()

    registry.register(
        "calculator",
        tool
    )

    result = registry.unregister(
        "calculator"
    )

    assert result is True
    assert registry.exists("calculator") is False
    assert registry.count() == 0


def test_unregister_unknown_tool():

    registry = create_registry()

    assert registry.unregister(
        "unknown"
    ) is False


def test_list_tools():

    registry = create_registry()

    registry.register(
        "calculator",
        MockTool()
    )

    registry.register(
        "python",
        MockTool()
    )

    assert registry.list_tools() == [
        "calculator",
        "python"
    ]


def test_get_tool_definitions():

    registry = create_registry()

    registry.register(
        "calculator",
        MockTool()
    )

    definitions = registry.get_definitions()

    assert definitions == [
        {
            "name": "calculator",
            "description": "Mock tool"
        }
    ]


def test_count_tools():

    registry = create_registry()

    assert registry.count() == 0

    registry.register(
        "calculator",
        MockTool()
    )

    registry.register(
        "python",
        MockTool()
    )

    assert registry.count() == 2


def test_clear_registry():

    registry = create_registry()

    registry.register(
        "calculator",
        MockTool()
    )

    registry.register(
        "python",
        MockTool()
    )

    registry.clear()

    assert registry.count() == 0
    assert registry.list_tools() == []