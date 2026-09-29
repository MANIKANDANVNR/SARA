import json
from pathlib import Path


class MemoryStore:

    def __init__(self, memory_file):

        self.memory_file = Path(memory_file)

    def initialize(self):

        self.memory_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.memory_file.exists():

            self._write([])

    def _write(self, memories):

        with open(
            self.memory_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memories,
                file,
                indent=4,
                ensure_ascii=False
            )

    def save(self, memories):

        self.initialize()

        self._write(memories)

        return True

    def load(self):

        self.initialize()

        try:

            with open(
                self.memory_file,
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

    def clear(self):

        self._write([])

        return True