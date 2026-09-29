from pathlib import Path

import pytest

from tools.file_write_tool import (
    FileWriteTool
)


def test_tool_name():

    tool = FileWriteTool()

    assert tool.name == "file_write"


def test_tool_description():

    tool = FileWriteTool()

    assert tool.description


def test_empty_path_rejected():

    tool = FileWriteTool()

    with pytest.raises(ValueError):

        tool.execute(
            "",
            "hello"
        )


def test_none_path_rejected():

    tool = FileWriteTool()

    with pytest.raises(ValueError):

        tool.execute(
            None,
            "hello"
        )


def test_none_content_rejected():

    tool = FileWriteTool()

    with pytest.raises(ValueError):

        tool.execute(
            "test.txt",
            None
        )


def test_creates_new_file(tmp_path):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "test.txt"
    )

    result = tool.execute(
        file_path,
        "Hello SARA"
    )

    assert file_path.exists()

    assert (
        file_path.read_text(
            encoding="utf-8"
        )
        == "Hello SARA"
    )

    assert result == str(
        file_path.resolve()
    )


def test_writes_multiline_content(tmp_path):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "multiline.txt"
    )

    content = (
        "Line 1\n"
        "Line 2\n"
        "Line 3"
    )

    tool.execute(
        file_path,
        content
    )

    assert (
        file_path.read_text(
            encoding="utf-8"
        )
        == content
    )


def test_overwrites_existing_file(tmp_path):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "existing.txt"
    )

    file_path.write_text(
        "Old content",
        encoding="utf-8"
    )

    tool.execute(
        file_path,
        "New content"
    )

    assert (
        file_path.read_text(
            encoding="utf-8"
        )
        == "New content"
    )


def test_custom_encoding(tmp_path):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "encoded.txt"
    )

    content = "Hello SARA"

    tool.execute(
        file_path,
        content,
        encoding="utf-16"
    )

    assert (
        file_path.read_text(
            encoding="utf-16"
        )
        == content
    )


def test_invalid_encoding_rejected(tmp_path):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "invalid.txt"
    )

    with pytest.raises(ValueError):

        tool.execute(
            file_path,
            "hello",
            encoding="invalid-encoding"
        )


def test_directory_rejected(tmp_path):

    tool = FileWriteTool()

    directory = (
        tmp_path /
        "directory"
    )

    directory.mkdir()

    with pytest.raises(ValueError):

        tool.execute(
            directory,
            "hello"
        )


def test_large_content_rejected(tmp_path):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "large.txt"
    )

    content = (
        "A" *
        (
            FileWriteTool.MAX_FILE_SIZE
            + 1
        )
    )

    with pytest.raises(ValueError):

        tool.execute(
            file_path,
            content
        )

    assert not file_path.exists()


def test_failed_write_does_not_create_file(
    tmp_path
):

    tool = FileWriteTool()

    file_path = (
        tmp_path /
        "failed.txt"
    )

    with pytest.raises(ValueError):

        tool.execute(
            file_path,
            "hello",
            encoding="invalid-encoding"
        )

    assert not file_path.exists()