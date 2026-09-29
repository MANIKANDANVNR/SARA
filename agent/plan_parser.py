import json


class AgentPlanParser:

    def parse(
        self,
        response
    ):

        if response is None:

            raise ValueError(
                "Agent plan response cannot be empty."
            )

        response = str(
            response
        ).strip()

        if not response:

            raise ValueError(
                "Agent plan response cannot be empty."
            )

        try:

            plan = json.loads(
                response
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                "Agent plan response must "
                "contain valid JSON."
            ) from error

        if not isinstance(
            plan,
            dict
        ):

            raise ValueError(
                "Agent plan response must "
                "be a JSON object."
            )

        return plan