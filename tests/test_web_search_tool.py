from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

import pytest

from tools.web_search_tool import WebSearchTool


def test_web_search_tool_name():

    tool = WebSearchTool()

    assert tool.name == "web_search"


def test_web_search_tool_description():

    tool = WebSearchTool()

    assert "searches the web" in tool.description


def test_empty_query_rejected():

    tool = WebSearchTool()

    with pytest.raises(
        ValueError,
        match="Search query cannot be empty."
    ):

        tool.execute("")


def test_none_query_rejected():

    tool = WebSearchTool()

    with pytest.raises(
        ValueError,
        match="Search query cannot be empty."
    ):

        tool.execute(None)


def test_query_too_long_rejected():

    tool = WebSearchTool()

    query = "a" * 501

    with pytest.raises(
        ValueError,
        match="Search query is too long"
    ):

        tool.execute(query)


def test_invalid_result_count_rejected():

    tool = WebSearchTool()

    with pytest.raises(
        ValueError,
        match="Maximum results must be an integer"
    ):

        tool.execute(
            "Python",
            max_results="invalid"
        )


def test_result_count_below_one_rejected():

    tool = WebSearchTool()

    with pytest.raises(
        ValueError,
        match="Maximum results must be at least 1"
    ):

        tool.execute(
            "Python",
            max_results=0
        )


def test_result_count_limited_to_maximum():

    tool = WebSearchTool()

    mock_response = Mock()

    mock_response.read.return_value = (
        b"<html></html>"
    )

    mock_response.__enter__ = Mock(
        return_value=mock_response
    )

    mock_response.__exit__ = Mock(
        return_value=False
    )

    with patch(
        "tools.web_search_tool.urlopen",
        return_value=mock_response
    ) as mocked_urlopen:

        result = tool.execute(
            "Python",
            max_results=100
        )

    assert result == []

    mocked_urlopen.assert_called_once()


def test_successful_search_returns_results():

    tool = WebSearchTool()

    html = """
    <div>
        <h3>Python Official Website</h3>
        <a href="https://www.python.org/">Python</a>
    </div>

    <div>
        <h3>Python Documentation</h3>
        <a href="https://docs.python.org/">Documentation</a>
    </div>
    """

    mock_response = Mock()

    mock_response.read.return_value = (
        html.encode("utf-8")
    )

    mock_response.__enter__ = Mock(
        return_value=mock_response
    )

    mock_response.__exit__ = Mock(
        return_value=False
    )

    with patch(
        "tools.web_search_tool.urlopen",
        return_value=mock_response
    ):

        result = tool.execute(
            "Python",
            max_results=2
        )

    assert len(result) == 2

    assert result[0]["title"] == (
        "Python Official Website"
    )

    assert result[0]["url"] == (
        "https://www.python.org/"
    )

    assert result[1]["title"] == (
        "Python Documentation"
    )

    assert result[1]["url"] == (
        "https://docs.python.org/"
    )


def test_search_respects_requested_result_limit():

    tool = WebSearchTool()

    html = """
    <div>
        <h3>Result One</h3>
        <a href="https://example.com/one">One</a>
    </div>

    <div>
        <h3>Result Two</h3>
        <a href="https://example.com/two">Two</a>
    </div>

    <div>
        <h3>Result Three</h3>
        <a href="https://example.com/three">Three</a>
    </div>
    """

    mock_response = Mock()

    mock_response.read.return_value = (
        html.encode("utf-8")
    )

    mock_response.__enter__ = Mock(
        return_value=mock_response
    )

    mock_response.__exit__ = Mock(
        return_value=False
    )

    with patch(
        "tools.web_search_tool.urlopen",
        return_value=mock_response
    ):

        result = tool.execute(
            "test",
            max_results=2
        )

    assert len(result) == 2


def test_http_error_is_handled():

    tool = WebSearchTool()

    error = HTTPError(
        url="https://www.google.com/",
        code=500,
        msg="Server Error",
        hdrs=None,
        fp=None
    )

    with patch(
        "tools.web_search_tool.urlopen",
        side_effect=error
    ):

        with pytest.raises(
            RuntimeError,
            match="HTTP status 500"
        ):

            tool.execute("Python")


def test_url_error_is_handled():

    tool = WebSearchTool()

    error = URLError(
        "Connection failed"
    )

    with patch(
        "tools.web_search_tool.urlopen",
        side_effect=error
    ):

        with pytest.raises(
            RuntimeError,
            match="Unable to connect to the web"
        ):

            tool.execute("Python")


def test_timeout_is_handled():

    tool = WebSearchTool()

    with patch(
        "tools.web_search_tool.urlopen",
        side_effect=TimeoutError()
    ):

        with pytest.raises(
            RuntimeError,
            match="timed out"
        ):

            tool.execute("Python")


def test_html_entities_are_cleaned():

    tool = WebSearchTool()

    result = tool._clean_html(
        "<b>Python &amp; Programming</b>"
    )

    assert result == (
        "Python & Programming"
    )


def test_html_tags_are_removed():

    tool = WebSearchTool()

    result = tool._clean_html(
        "<span>Hello</span> <strong>World</strong>"
    )

    assert result == "Hello World"