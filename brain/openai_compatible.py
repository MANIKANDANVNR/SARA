import json
import urllib.error
import urllib.request

from brain.provider import AIProvider


class OpenAICompatibleProvider(AIProvider):

    name = "openai_compatible"

    def __init__(
        self,
        base_url,
        model,
        api_key="",
        timeout=120,
        max_tokens=1000,
        temperature=0.7
    ):

        self.base_url = base_url.rstrip("/")

        self.model = model

        self.api_key = api_key

        self.timeout = timeout

        self.max_tokens = max_tokens

        self.temperature = temperature

    def _headers(self):

        headers = {
            "Content-Type": "application/json"
        }

        if self.api_key:

            headers["Authorization"] = (
                f"Bearer {self.api_key}"
            )

        return headers

    def health_check(self):

        url = (
            f"{self.base_url}/models"
        )

        request = urllib.request.Request(
            url,
            headers=self._headers(),
            method="GET"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=self.timeout
            ) as response:

                return (
                    200
                    <= response.status
                    < 300
                )

        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError
        ):

            return False

    def generate(
        self,
        prompt,
        context=None
    ):

        messages = []

        if context:

            messages.append({
                "role": "system",
                "content": (
                    "You are SARA, a personal AI "
                    "assistant. Use the supplied "
                    "context when relevant. "
                    "Do not claim to have performed "
                    "actions that you did not perform."
                    "\n\n"
                    "CONTEXT:\n"
                    f"{context}"
                )
            })

        else:

            messages.append({
                "role": "system",
                "content": (
                    "You are SARA, a personal AI "
                    "assistant. Be accurate, clear, "
                    "and honest about your capabilities."
                )
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        data = json.dumps(
            payload
        ).encode("utf-8")

        url = (
            f"{self.base_url}/chat/completions"
        )

        request = urllib.request.Request(
            url,
            data=data,
            headers=self._headers(),
            method="POST"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=self.timeout
            ) as response:

                raw = response.read()

                result = json.loads(
                    raw.decode("utf-8")
                )

        except urllib.error.HTTPError as error:

            body = error.read().decode(
                "utf-8",
                errors="replace"
            )

            raise RuntimeError(
                f"AI provider HTTP error "
                f"{error.code}: {body}"
            )

        except (
            urllib.error.URLError,
            TimeoutError
        ) as error:

            raise RuntimeError(
                f"AI provider connection failed: "
                f"{error}"
            )

        choices = result.get(
            "choices",
            []
        )

        if not choices:

            raise RuntimeError(
                "AI provider returned no response."
            )

        message = choices[0].get(
            "message",
            {}
        )

        content = message.get(
            "content"
        )

        if not content:

            raise RuntimeError(
                "AI provider returned empty content."
            )

        return content.strip()