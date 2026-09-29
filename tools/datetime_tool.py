from datetime import datetime


class DateTimeTool:

    name = "datetime"

    description = (
        "Provides the current local date and time."
    )

    def execute(self):

        now = datetime.now()

        return {
            "date": now.strftime(
                "%Y-%m-%d"
            ),
            "time": now.strftime(
                "%H:%M:%S"
            ),
            "datetime": now.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "day": now.strftime(
                "%A"
            )
        }