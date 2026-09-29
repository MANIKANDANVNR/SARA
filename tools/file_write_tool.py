from pathlib import Path


class FileWriteTool:

    name = "file_write"

    description = (
        "Safely writes text content to a local filesystem file."
    )

    MAX_FILE_SIZE = 1024 * 1024

    DEFAULT_ENCODING = "utf-8"

    def execute(
        self,
        path,
        content,
        encoding=None
    ):

        if path is None:

            raise ValueError(
                "File path cannot be empty."
            )

        path = str(
            path
        ).strip()

        if not path:

            raise ValueError(
                "File path cannot be empty."
            )

        if content is None:

            raise ValueError(
                "File content cannot be empty."
            )

        content = str(
            content
        )

        selected_encoding = (
            encoding
            if encoding
            else self.DEFAULT_ENCODING
        )

        selected_encoding = str(
            selected_encoding
        ).strip()

        if not selected_encoding:

            selected_encoding = (
                self.DEFAULT_ENCODING
            )

        try:

            encoded_content = content.encode(
                selected_encoding
            )

        except LookupError as error:

            raise ValueError(
                "Unable to encode the file "
                f"using {selected_encoding}."
            ) from error

        except UnicodeEncodeError as error:

            raise ValueError(
                "Unable to encode the file "
                f"using {selected_encoding}."
            ) from error

        if len(encoded_content) > self.MAX_FILE_SIZE:

            raise ValueError(
                "File content is too large to write. "
                "Maximum size is 1 MB."
            )

        file_path = Path(
            path
        )

        try:

            file_path = (
                file_path
                .expanduser()
                .resolve()
            )

        except (
            OSError,
            RuntimeError
        ) as error:

            raise ValueError(
                "Invalid file path."
            ) from error

        if file_path.exists() and file_path.is_dir():

            raise ValueError(
                "The specified path is a directory."
            )

        try:

            file_path.write_text(
                content,
                encoding=selected_encoding
            )

        except UnicodeEncodeError as error:

            raise ValueError(
                "Unable to encode the file "
                f"using {selected_encoding}."
            ) from error

        except LookupError as error:

            raise ValueError(
                "Unable to encode the file "
                f"using {selected_encoding}."
            ) from error

        except OSError as error:

            raise ValueError(
                "Unable to write the file."
            ) from error

        return str(
            file_path
        )