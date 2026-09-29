import json
from pathlib import Path


class ProfileStore:

    def __init__(self, profile_file):

        self.profile_file = Path(
            profile_file
        )

    # -------------------------------------------------
    # INITIALIZE
    # -------------------------------------------------

    def initialize(self):

        self.profile_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.profile_file.exists():

            self._write({})

    # -------------------------------------------------
    # WRITE
    # -------------------------------------------------

    def _write(self, profile):

        with open(
            self.profile_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                profile,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------

    def save(self, profile):

        self.initialize()

        self._write(profile)

        return True

    # -------------------------------------------------
    # LOAD
    # -------------------------------------------------

    def load(self):

        self.initialize()

        try:

            with open(
                self.profile_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, dict):

                    return data

                return {}

        except (
            json.JSONDecodeError,
            OSError
        ):

            return {}

    # -------------------------------------------------
    # CLEAR
    # -------------------------------------------------

    def clear(self):

        self.initialize()

        self._write({})

        return True