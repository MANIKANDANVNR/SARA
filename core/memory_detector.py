class MemoryDetector:

    IMPORTANT_PATTERNS = {
        "personal": {
            "my name is",
            "my age is",
            "my birthday is",
            "my family",
            "my father",
            "my mother",
            "my brother",
            "my sister",
            "i live in",
            "i am from",
        },

        "preferences": {
            "i like",
            "i love",
            "i prefer",
            "i don't like",
            "i dislike",
            "my favorite",
            "i hate",
        },

        "career": {
            "my job",
            "my career",
            "my goal is",
            "my salary",
            "i work as",
            "i work at",
            "i want to become",
            "i want a job",
            "job",
            "career",
            "resume",
            "developer job",
            "python developer job",
            "software developer job",
            "data analyst job",
            "data analyst",
            "python developer",
            "software developer",
        },

        "projects": {
            "my project",
            "i am building",
            "i'm building",
            "i am developing",
            "i'm developing",
            "my application",
            "my app",
            "my website",
            "my game",
            "my ai",
        },

        "technical": {
            "i use python",
            "i use sql",
            "i use mysql",
            "i use power bi",
            "i am learning python",
            "i'm learning python",
            "i am learning sql",
            "i'm learning sql",
            "i am learning programming",
            "i'm learning programming",
        }
    }

    def __init__(self):

        self.last_category = None

    # -------------------------------------------------
    # DETECT
    # -------------------------------------------------

    def detect(self, content):

        if not content:

            return None

        text = (
            str(content)
            .strip()
            .lower()
        )

        if not text:

            return None

        # Questions should never be stored
        # as automatic long-term memories.

        if self._is_question(text):

            self.last_category = None

            return None

        # Memory-management commands should
        # never be stored as automatic memories.

        if self._is_memory_command(text):

            self.last_category = None

            return None

        # Check longer/more specific
        # patterns first.

        patterns = []

        for category, category_patterns in (
            self.IMPORTANT_PATTERNS.items()
        ):

            for pattern in category_patterns:

                patterns.append(
                    (
                        len(pattern),
                        category,
                        pattern
                    )
                )

        patterns.sort(
            reverse=True
        )

        for (
            _,
            category,
            pattern
        ) in patterns:

            if pattern in text:

                self.last_category = category

                return {
                    "important": True,
                    "category": category,
                    "content": str(content).strip()
                }

        self.last_category = None

        return None

    # -------------------------------------------------
    # QUESTION CHECK
    # -------------------------------------------------

    def _is_question(self, text):

        if not text:

            return False

        if text.endswith("?"):

            return True

        question_prefixes = (
            "what ",
            "what's ",
            "whats ",
            "who ",
            "who's ",
            "whos ",
            "where ",
            "where's ",
            "wheres ",
            "when ",
            "when's ",
            "whens ",
            "why ",
            "how ",
            "how's ",
            "hows ",
            "which ",
            "can you ",
            "could you ",
            "would you ",
            "do you ",
            "did you ",
            "are you ",
            "is it ",
            "is my ",
            "am i ",
        )

        return text.startswith(
            question_prefixes
        )

    # -------------------------------------------------
    # MEMORY COMMAND CHECK
    # -------------------------------------------------

    def _is_memory_command(self, text):

        if not text:

            return False

        memory_commands = (
            "remember ",
            "recall ",
            "forget ",
            "clear memory",
            "clear memories",
            "delete memory",
            "delete memories",
        )

        return text.startswith(
            memory_commands
        )

    # -------------------------------------------------
    # IMPORTANT CHECK
    # -------------------------------------------------

    def is_important(self, content):

        result = self.detect(content)

        return result is not None

    # -------------------------------------------------
    # CATEGORY
    # -------------------------------------------------

    def detect_category(self, content):

        result = self.detect(content)

        if result is None:

            return "general"

        return result["category"]