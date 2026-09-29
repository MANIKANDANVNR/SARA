import json
import urllib.error
import urllib.request

from brain.provider import AIProvider


class OllamaProvider(AIProvider):

    name = "ollama"

    def __init__(
        self,
        base_url="http://127.0.0.1:11434",
        model="qwen2.5:3b",
        timeout=120,
        temperature=0.7
    ):

        self.base_url = base_url.rstrip("/")

        self.model = model

        self.timeout = timeout

        self.temperature = temperature

    def health_check(self):

        url = f"{self.base_url}/api/tags"

        request = urllib.request.Request(
            url,
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
        context=None,
        format=None
    ):

        if context:

            system_message = (
                "You are SARA, a personal AI "
                "assistant. Use the supplied "
                "context when relevant. "
                "Do not claim to have performed "
                "actions that you did not perform."
                "\n\n"
                "CONTEXT:\n"
                f"{context}"
            )

        else:

            system_message = (
                "You are SARA, a personal AI "
                "assistant. Be accurate, clear, "
                "and honest about your capabilities."
            )

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }

        if format is not None:

            payload["format"] = format

        data = json.dumps(
            payload
        ).encode("utf-8")

        url = f"{self.base_url}/api/chat"

        request = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json"
            },
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
                f"Ollama HTTP error "
                f"{error.code}: {body}"
            )

        except (
            urllib.error.URLError,
            TimeoutError
        ) as error:

            raise RuntimeError(
                f"Ollama connection failed: "
                f"{error}"
            )

        message = result.get(
            "message",
            {}
        )

        content = message.get(
            "content"
        )

        if not content:

            raise RuntimeError(
                "Ollama returned empty content."
            )

        return content.strip()