class ConversationManager:

    def __init__(
        self,
        max_messages=20
    ):

        self.max_messages = max_messages

        self.messages = []

    # -------------------------------------------------
    # ADD MESSAGE
    # -------------------------------------------------

    def add_user_message(self, content):

        if not content:
            return False

        self.messages.append({
            "role": "user",
            "content": content
        })

        self._enforce_limit()

        return True

    def add_assistant_message(self, content):

        if not content:
            return False

        self.messages.append({
            "role": "assistant",
            "content": content
        })

        self._enforce_limit()

        return True

    # -------------------------------------------------
    # LOAD MESSAGES
    # -------------------------------------------------

    def load_messages(self, messages):

        if not isinstance(messages, list):

            self.messages = []

            return False

        self.messages = []

        for message in messages:

            if not isinstance(message, dict):
                continue

            role = message.get("role")

            content = message.get("content")

            if role not in {
                "user",
                "assistant"
            }:
                continue

            if not content:
                continue

            self.messages.append({
                "role": role,
                "content": content
            })

        self._enforce_limit()

        return True

    # -------------------------------------------------
    # GET CONVERSATION
    # -------------------------------------------------

    def get_messages(self):

        return list(self.messages)

    def get_recent_messages(
        self,
        limit=None
    ):

        if limit is None:

            limit = self.max_messages

        if limit <= 0:

            return []

        return self.messages[-limit:]

    # -------------------------------------------------
    # CONVERSATION STATE
    # -------------------------------------------------

    def message_count(self):

        return len(self.messages)

    def clear(self):

        self.messages.clear()

    # -------------------------------------------------
    # LIMIT
    # -------------------------------------------------

    def _enforce_limit(self):

        if self.max_messages <= 0:

            self.messages.clear()

            return

        if (
            len(self.messages)
            > self.max_messages
        ):

            self.messages = (
                self.messages[
                    -self.max_messages:
                ]
            )