class ContextManager:

    def __init__(
        self,
        memory_manager,
        conversation_manager=None,
        profile_manager=None,
        max_recent_messages=10,
        max_long_term_memories=5
    ):

        self.memory_manager = (
            memory_manager
        )

        self.conversation_manager = (
            conversation_manager
        )

        self.profile_manager = (
            profile_manager
        )

        self.max_recent_messages = (
            max_recent_messages
        )

        self.max_long_term_memories = (
            max_long_term_memories
        )

    # -------------------------------------------------
    # CONTEXT BUILDING
    # -------------------------------------------------

    def build_context(self, query):

        context = {
            "query": query,
            "short_term": [],
            "long_term": [],
            "conversation": [],
            "profile": {}
        }

        # SHORT-TERM MEMORY

        short_term = (
            self.memory_manager
            .get_short_term()
        )

        if self.max_recent_messages > 0:

            short_term = short_term[
                -self.max_recent_messages:
            ]

        context["short_term"] = short_term

        # CONVERSATION

        if self.conversation_manager:

            conversation = (
                self.conversation_manager
                .get_recent_messages(
                    self.max_recent_messages
                )
            )

            context["conversation"] = (
                conversation
            )

        # LONG-TERM MEMORY

        long_term = (
            self.memory_manager
            .search_long_term(query)
        )

        if self.max_long_term_memories > 0:

            long_term = long_term[
                :self.max_long_term_memories
            ]

        context["long_term"] = long_term

        # PROFILE

        if self.profile_manager:

            context["profile"] = (
                self.profile_manager
                .get_all()
            )

        return context

    # -------------------------------------------------
    # RELEVANT MEMORIES
    # -------------------------------------------------

    def get_relevant_memories(
        self,
        query
    ):

        memories = (
            self.memory_manager
            .search_long_term(query)
        )

        if self.max_long_term_memories > 0:

            return memories[
                :self.max_long_term_memories
            ]

        return memories

    # -------------------------------------------------
    # FORMATTING
    # -------------------------------------------------

    def format_context(self, query):

        context = self.build_context(
            query
        )

        lines = []

        lines.append(
            f"Current request: {context['query']}"
        )

        # PROFILE

        if context["profile"]:

            lines.append("")

            lines.append(
                "User profile:"
            )

            for key, value in (
                context["profile"].items()
            ):

                lines.append(
                    f"- {key}: {value}"
                )

        # CONVERSATION

        if context["conversation"]:

            lines.append("")

            lines.append(
                "Current conversation:"
            )

            for message in (
                context["conversation"]
            ):

                role = message["role"]

                content = message["content"]

                if role == "user":

                    lines.append(
                        f"User: {content}"
                    )

                elif role == "assistant":

                    lines.append(
                        f"SARA: {content}"
                    )

        # SHORT-TERM MEMORY

        if context["short_term"]:

            lines.append("")

            lines.append(
                "Recent memory:"
            )

            for memory in (
                context["short_term"]
            ):

                lines.append(
                    f"- {memory['content']}"
                )

        # LONG-TERM MEMORY

        if context["long_term"]:

            lines.append("")

            lines.append(
                "Relevant long-term memory:"
            )

            for memory in (
                context["long_term"]
            ):

                lines.append(
                    f"- [{memory['category']}] "
                    f"{memory['content']}"
                )

        return "\n".join(lines)