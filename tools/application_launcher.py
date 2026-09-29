import os
import subprocess


class ApplicationLauncher:

    name = "application_launcher"

    description = (
        "Safely launches approved desktop applications "
        "using a fixed application allowlist."
    )

    APPLICATIONS = {
        "notepad": {
            "command": ["notepad.exe"]
        },
        "calculator": {
            "command": ["calc.exe"]
        },
        "explorer": {
            "command": ["explorer.exe"]
        },
        "chrome": {
            "command": [
                "cmd",
                "/c",
                "start",
                "",
                "chrome"
            ]
        },
        "vscode": {
            "command": [
                "code"
            ]
        },
        "pycharm": {
            "command": [
                "pycharm64.exe"
            ]
        }
    }

    def execute(
        self,
        application
    ):

        # -----------------------------------------
        # VALIDATE APPLICATION
        # -----------------------------------------

        if application is None:

            raise ValueError(
                "Application name cannot be empty."
            )

        application = str(
            application
        ).strip().lower()

        if not application:

            raise ValueError(
                "Application name cannot be empty."
            )

        # -----------------------------------------
        # CHECK ALLOWLIST
        # -----------------------------------------

        if application not in self.APPLICATIONS:

            raise ValueError(
                f"Application '{application}' "
                "is not allowed."
            )

        configuration = self.APPLICATIONS[
            application
        ]

        command = configuration[
            "command"
        ]

        # -----------------------------------------
        # LAUNCH APPLICATION
        # -----------------------------------------

        try:

            process = subprocess.Popen(
                command,
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        except (
            FileNotFoundError,
            OSError
        ) as error:

            raise RuntimeError(
                f"Unable to launch "
                f"'{application}'."
            ) from error

        return {
            "application": application,
            "pid": process.pid,
            "launched": True
        }