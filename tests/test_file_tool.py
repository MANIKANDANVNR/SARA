from pathlib import Path

import pytest

from tools.file_tool import FileTool


class TestFileTool:

    def test_tool_name(self):

        tool = FileTool()

        assert tool.name == "file"

    def test_tool_description(self):

        tool = FileTool()

        assert isinstance(
            tool.description,
            str
        )

        assert tool.description

    def test_empty_path_is_rejected(self):

        tool = FileTool()

        with pytest.raises(
            ValueError,
            match="File path cannot be empty"
        ):

            tool.execute("")

    def test_none_path_is_rejected(self):

        tool = FileTool()

        with pytest.raises(
            ValueError,
            match="File path cannot be empty"
        ):

            tool.execute(None)

    def test_missing_file_is_rejected(
        self,
        tmp_path
    ):

        tool = FileTool()

        missing_file = (
            tmp_path / "missing.txt"
        )

        with pytest.raises(
            FileNotFoundError,
            match="File not found"
        ):

            tool.execute(
                str(missing_file)
            )

    def test_directory_is_rejected(
        self,
        tmp_path
    ):

        tool = FileTool()

        directory = (
            tmp_path / "folder"
        )

        directory.mkdir()

        with pytest.raises(
            ValueError,
            match="not a file"
        ):

            tool.execute(
                str(directory)
            )

    def test_reads_text_file(
        self,
        tmp_path
    ):

        tool = FileTool()

        test_file = (
            tmp_path / "test.txt"
        )

        test_file.write_text(
            "Hello SARA!",
            encoding="utf-8"
        )

        result = tool.execute(
            str(test_file)
        )

        assert result == "Hello SARA!"

    def test_reads_multiline_file(
        self,
        tmp_path
    ):

        tool = FileTool()

        test_file = (
            tmp_path / "test.txt"
        )

        content = (
            "Line one\n"
            "Line two\n"
            "Line three"
        )

        test_file.write_text(
            content,
            encoding="utf-8"
        )

        result = tool.execute(
            str(test_file)
        )

        assert result == content

    def test_supports_custom_encoding(
        self,
        tmp_path
    ):

        tool = FileTool()

        test_file = (
            tmp_path / "test.txt"
        )

        content = "SARA – Tamil Nadu"

        test_file.write_text(
            content,
            encoding="utf-16"
        )

        result = tool.execute(
            str(test_file),
            encoding="utf-16"
        )

        assert result == content

    def test_invalid_encoding_is_rejected(
        self,
        tmp_path
    ):

        tool = FileTool()

        test_file = (
            tmp_path / "test.txt"
        )

        test_file.write_text(
            "Hello",
            encoding="utf-8"
        )

        with pytest.raises(
            ValueError,
            match="Unable to decode"
        ):

            tool.execute(
                str(test_file),
                encoding="invalid-encoding"
            )

    def test_large_file_is_rejected(
        self,
        tmp_path
    ):

        tool = FileTool()

        test_file = (
            tmp_path / "large.txt"
        )

        test_file.write_bytes(
            b"x" * (
                FileTool.MAX_FILE_SIZE + 1
            )
        )

        with pytest.raises(
            ValueError,
            match="File is too large"
        ):

            tool.execute(
                str(test_file)
            )

    def test_file_tool_does_not_modify_file(
        self,
        tmp_path
    ):

        tool = FileTool()

        test_file = (
            tmp_path / "readonly_test.txt"
        )

        original_content = (
            "Original SARA content"
        )

        test_file.write_text(
            original_content,
            encoding="utf-8"
        )

        result = tool.execute(
            str(test_file)
        )

        assert result == original_content

        assert (
            test_file.read_text(
                encoding="utf-8"
            )
            == original_content
        )