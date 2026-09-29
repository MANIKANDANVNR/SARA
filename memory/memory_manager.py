from datetime import datetime


class MemoryManager:

    DEFAULT_CATEGORIES = {
        "personal",
        "preferences",
        "career",
        "projects",
        "technical",
        "general"
    }

    def __init__(
        self,
        max_short_term=20
    ):

        self.max_short_term = (
            max_short_term
        )

        self.short_term_memory = []

        self.long_term_memory = []

    # -------------------------------------------------
    # SHORT-TERM MEMORY
    # -------------------------------------------------

    def remember_short_term(self, content):

        if not content:
            return False

        entry = {
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        self.short_term_memory.append(entry)

        if (
            len(self.short_term_memory)
            > self.max_short_term
        ):

            self.short_term_memory.pop(0)

        return True

    def get_short_term(self):

        return list(self.short_term_memory)

    def clear_short_term(self):

        self.short_term_memory.clear()

    # -------------------------------------------------
    # LONG-TERM MEMORY
    # -------------------------------------------------

    def remember_long_term(
        self,
        content,
        category="general"
    ):

        if not content:
            return False

        category = (
            str(category)
            .strip()
            .lower()
        )

        if category not in self.DEFAULT_CATEGORIES:

            category = "general"

        entry = {
            "content": content,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

        self.long_term_memory.append(entry)

        return True

    def get_long_term(self):

        return list(self.long_term_memory)

    def delete_long_term(self, index):

        if (
            index < 0
            or index >= len(
                self.long_term_memory
            )
        ):

            return False

        self.long_term_memory.pop(index)

        return True

    def clear_long_term(self):

        self.long_term_memory.clear()

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    def search_long_term(self, query):

        if not query:
            return []

        query = str(query).strip().lower()

        if not query:
            return []

        import re

        def normalize(text):

            text = str(text).lower()

            text = re.sub(
                r"[^\w\s]",
                " ",
                text
            )

            return " ".join(
                text.split()
            )

        stop_words = {
            "a",
            "an",
            "and",
            "am",
            "are",
            "as",
            "at",
            "be",
            "for",
            "i",
            "in",
            "is",
            "it",
            "me",
            "my",
            "of",
            "on",
            "that",
            "the",
            "to",
            "was",
            "what",
            "with"
        }

        normalized_query = normalize(query)

        query_words = {
            word
            for word in normalized_query.split()
            if word not in stop_words
        }

        if not query_words:
            return []

        results = []

        for memory in self.long_term_memory:

            content = normalize(
                memory.get("content", "")
            )

            category = normalize(
                memory.get("category", "general")
            )

            content_words = set(
                content.split()
            )

            if (
                    normalized_query in content
                    or normalized_query in category
            ):
                results.append(memory)
                continue

            matched_words = (
                    query_words & content_words
            )

            if (
                    matched_words
                    and matched_words == query_words
            ):
                results.append(memory)

        return results

    def search_by_category(
        self,
        category
    ):

        if not category:
            return []

        category = (
            str(category)
            .strip()
            .lower()
        )

        return [
            memory
            for memory in self.long_term_memory
            if memory.get(
                "category",
                "general"
            ).lower() == category
        ]

    # -------------------------------------------------
    # GENERAL
    # -------------------------------------------------

    def count_short_term(self):

        return len(
            self.short_term_memory
        )

    def count_long_term(self):

        return len(
            self.long_term_memory
        )

    def clear_all(self):

        self.clear_short_term()

        self.clear_long_term()