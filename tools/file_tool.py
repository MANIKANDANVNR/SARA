from pathlib import Path


class FileTool:

    name = "file"

    description = (
        "Safely reads text files from the local filesystem."
    )

    MAX_FILE_SIZE = 1024 * 1024

    DEFAULT_ENCODING = "utf-8"

    def execute(
        self,
        path,
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

        if not file_path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():

            raise ValueError(
                "The specified path is not a file."
            )

        try:

            file_size = (
                file_path.stat().st_size
            )

        except OSError as error:

            raise ValueError(
                "Unable to access the file."
            ) from error

        if file_size > self.MAX_FILE_SIZE:

            raise ValueError(
                "File is too large to read. "
                "Maximum size is 1 MB."
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

            return file_path.read_text(
                encoding=selected_encoding
            )

        except UnicodeDecodeError as error:

            raise ValueError(
                "Unable to decode the file "
                f"using {selected_encoding}."
            ) from error

        except LookupError as error:

            raise ValueError(
                "Unable to decode the file "
                f"using {selected_encoding}."
            ) from error

        except OSError as error:

            raise ValueError(
                "Unable to read the file."
            ) from error