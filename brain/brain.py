from typing import Optional


class SaraBrain:

    def __init__(self, provider=None):

        self.provider = provider

        self.available = False

        self.last_error: Optional[str] = None

    def initialize(self):

        if self.provider is None:

            self.available = False

            self.last_error = (
                "No AI provider configured."
            )

            return False

        try:

            self.available = self.provider.health_check()

            if not self.available:

                self.last_error = (
                    "AI provider is unavailable."
                )

            else:

                self.last_error = None

            return self.available

        except Exception as error:

            self.available = False

            self.last_error = str(error)

            return False

    def think(
        self,
        prompt: str,
        context: Optional[str] = None
    ):

        if not self.available:

            return (
                "My AI brain is not available yet."
            )

        if not prompt:

            return (
                "I need something to think about."
            )

        try:

            response = self.provider.generate(
                prompt=prompt,
                context=context
            )

            return response

        except Exception as error:

            self.last_error = str(error)

            return (
                "I encountered an error while "
                "processing your request."
            )

    def status(self):

        return {
            "available": self.available,
            "provider": (
                self.provider.name
                if self.provider
                else None
            ),
            "model": (
                self.provider.model
                if self.provider
                else None
            ),
            "last_error": self.last_error
        }