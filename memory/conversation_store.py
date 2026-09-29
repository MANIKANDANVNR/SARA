import json
from pathlib import Path


class ConversationStore:

    def __init__(self, conversation_file):

        self.conversation_file = Path(
            conversation_file
        )

    # -------------------------------------------------
    # INITIALIZE
    # -------------------------------------------------

    def initialize(self):

        self.conversation_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.conversation_file.exists():

            self._write([])

    # -------------------------------------------------
    # WRITE
    # -------------------------------------------------

    def _write(self, messages):

        with open(
            self.conversation_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                messages,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------

    def save(self, messages):

        self.initialize()

        self._write(messages)

        return True

    # -------------------------------------------------
    # LOAD
    # -------------------------------------------------

    def load(self):

        self.initialize()

        try:

            with open(
                self.conversation_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):

                    return data

                return []

        except (
            json.JSONDecodeError,
            OSError
        ):

            return []

    # -------------------------------------------------
    # CLEAR
    # -------------------------------------------------

    def clear(self):

        self.initialize()

        self._write([])

        return True