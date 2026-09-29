class AgentRecovery:

    RETRYABLE_ERRORS = {
        "execution failed.",
        "connection failed.",
        "timeout."
    }

    NON_RETRYABLE_ERRORS = {
        "permission denied.",
        "tool not found.",
        "unknown tool.",
        "invalid arguments."
    }

    def __init__(
        self,
        max_attempts=3
    ):

        if not isinstance(
            max_attempts,
            int
        ):

            raise ValueError(
                "Maximum attempts must be an integer."
            )

        if max_attempts < 1:

            raise ValueError(
                "Maximum attempts must be at least 1."
            )

        self.max_attempts = max_attempts

    def is_retryable(
        self,
        error
    ):

        if error is None:

            return False

        error = str(
            error
        ).strip().lower()

        if not error:

            return False

        if error in self.RETRYABLE_ERRORS:

            return True

        if error in self.NON_RETRYABLE_ERRORS:

            return False

        return False

    def can_retry(
        self,
        step,
        error
    ):

        if step is None:

            return False

        if not self.is_retryable(
            error
        ):

            return False

        return (
            step.attempts
            < self.max_attempts
        )