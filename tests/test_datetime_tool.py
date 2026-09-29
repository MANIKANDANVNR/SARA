from datetime import datetime

from tools.datetime_tool import (
    DateTimeTool
)


def test_datetime_tool_name():

    tool = DateTimeTool()

    assert tool.name == "datetime"


def test_datetime_tool_description():

    tool = DateTimeTool()

    assert isinstance(
        tool.description,
        str
    )

    assert tool.description


def test_datetime_tool_returns_dictionary():

    tool = DateTimeTool()

    result = tool.execute()

    assert isinstance(
        result,
        dict
    )


def test_datetime_tool_returns_required_fields():

    tool = DateTimeTool()

    result = tool.execute()

    assert "date" in result
    assert "time" in result
    assert "datetime" in result
    assert "day" in result


def test_datetime_tool_date_format():

    tool = DateTimeTool()

    result = tool.execute()

    datetime.strptime(
        result["date"],
        "%Y-%m-%d"
    )


def test_datetime_tool_time_format():

    tool = DateTimeTool()

    result = tool.execute()

    datetime.strptime(
        result["time"],
        "%H:%M:%S"
    )


def test_datetime_tool_datetime_format():

    tool = DateTimeTool()

    result = tool.execute()

    datetime.strptime(
        result["datetime"],
        "%Y-%m-%d %H:%M:%S"
    )


def test_datetime_tool_day_is_valid():

    tool = DateTimeTool()

    result = tool.execute()

    valid_days = {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    }

    assert result["day"] in valid_days


def test_datetime_tool_matches_current_date():

    tool = DateTimeTool()

    result = tool.execute()

    expected_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    assert result["date"] == expected_date


def test_datetime_tool_matches_current_time_structure():

    tool = DateTimeTool()

    result = tool.execute()

    expected = datetime.strptime(
        result["datetime"],
        "%Y-%m-%d %H:%M:%S"
    )

    now = datetime.now()

    difference = abs(
        (
            expected - now
        ).total_seconds()
    )

    assert difference < 2