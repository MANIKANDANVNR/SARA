from enum import Enum


class IntentType:

    AI = "ai"

    AGENT = "agent"

    AI_STATUS = "ai_status"

    SECURITY_STATUS = "security_status"

    AUTHENTICATE = "authenticate"

    AUTHENTICATE_STRONG = "authenticate_strong"

    AUTHENTICATE_CRITICAL = "authenticate_critical"

    LOGOUT = "logout"

    PERMISSIONS = "permissions"

    EMERGENCY_SHUTDOWN = "emergency_shutdown"

    CALCULATOR = "calculator"

    PYTHON = "python"

    FILE_WRITE = "file_write"

    DATETIME = "datetime"

    SYSTEM_INFO = "system_info"

    WEB_SEARCH = "web_search"

    APPLICATION_LAUNCH = "application_launch"

    MEMORY_STATUS = "memory_status"

    MEMORY_SHORT = "memory_short"

    MEMORY_LONG = "memory_long"

    MEMORY_CLEAR_SHORT = "memory_clear_short"

    MEMORY_CLEAR_LONG = "memory_clear_long"

    MEMORY_REMEMBER = "memory_remember"

    MEMORY_RECALL = "memory_recall"

    MEMORY_FORGET = "memory_forget"

    MEMORY_CATEGORY = "memory_category"

    CONVERSATION_STATUS = "conversation_status"

    CONVERSATION_CLEAR = "conversation_clear"

    PROFILE_STATUS = "profile_status"

    PROFILE_SET = "profile_set"

    PROFILE_CLEAR = "profile_clear"

    SHUTDOWN = "shutdown"

    UNKNOWN = "unknown"


class Intent:

    def __init__(
        self,
        intent_type,
        value=None
    ):

        self.type = intent_type

        self.value = value


class IntentRouter:

    def route(self, command):

        if not command:

            return Intent(
                IntentType.UNKNOWN
            )

        text = command.strip()

        if not text:

            return Intent(
                IntentType.UNKNOWN
            )

        lower = text.lower()

        # =================================================
        # SHUTDOWN
        # =================================================

        if lower in {
            "shutdown",
            "exit",
            "quit"
        }:

            return Intent(
                IntentType.SHUTDOWN
            )

        # =================================================
        # SECURITY STATUS
        # =================================================

        if lower in {
            "security",
            "security status"
        }:

            return Intent(
                IntentType.SECURITY_STATUS
            )

        # =================================================
        # AUTHENTICATION
        # =================================================

        if lower == "authenticate":

            return Intent(
                IntentType.AUTHENTICATE
            )

        if lower == "authenticate strong":

            return Intent(
                IntentType.AUTHENTICATE_STRONG
            )

        if lower == "authenticate critical":

            return Intent(
                IntentType.AUTHENTICATE_CRITICAL
            )

        # =================================================
        # LOGOUT
        # =================================================

        if lower == "logout":

            return Intent(
                IntentType.LOGOUT
            )

        # =================================================
        # PERMISSIONS
        # =================================================

        if lower in {
            "permissions",
            "permission",
            "permission status"
        }:

            return Intent(
                IntentType.PERMISSIONS
            )

        # =================================================
        # EMERGENCY SHUTDOWN
        # =================================================

        if lower == "emergency shutdown":

            return Intent(
                IntentType.EMERGENCY_SHUTDOWN
            )

        # =================================================
        # CALCULATOR
        # =================================================

        if lower == "calculate":
            return Intent(
                IntentType.UNKNOWN
            )

        if lower.startswith("calculate "):

            expression = text[
                len("calculate "):
            ].strip()

            if not expression:
                return Intent(
                    IntentType.UNKNOWN
                )

            natural_language_markers = [
                ",",
                " divide ",
                " add ",
                " subtract ",
                " multiply ",
                " increase ",
                " decrease ",
                " percent ",
                " percentage ",
                " times ",
                " step ",
                " steps ",
                " result ",
                " starting ",
                " then ",
                " first ",
                " each "
            ]

            if any(
                    marker in lower
                    for marker in natural_language_markers
            ):
                return Intent(
                    IntentType.AGENT,
                    text
                )

            return Intent(
                IntentType.CALCULATOR,
                expression
            )
        # =================================================
        # PYTHON
        # =================================================

        if lower == "python":

            return Intent(
                IntentType.UNKNOWN
            )

        if lower.startswith("python "):

            code = text[
                len("python "):
            ].strip()

            if not code:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.PYTHON,
                code
            )

        # =================================================
        # FILE WRITE
        # =================================================

        if lower == "write file":

            return Intent(
                IntentType.UNKNOWN
            )

        if lower.startswith("write file "):

            file_data = text[
                len("write file "):
            ].strip()

            if not file_data:

                return Intent(
                    IntentType.UNKNOWN
                )

            parts = file_data.split(
                maxsplit=1
            )

            if len(parts) != 2:

                return Intent(
                    IntentType.UNKNOWN
                )

            path = parts[0].strip()

            content = parts[1]

            if not path or not content:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.FILE_WRITE,
                {
                    "path": path,
                    "content": content
                }
            )

        # =================================================
        # DATE & TIME
        # =================================================

        if lower in {
            "date",
            "time",
            "date and time",
            "current date",
            "current time",
            "current date and time",
            "what is the date",
            "what is the time",
            "what is the current date",
            "what is the current time",
            "what is the current date and time",
            "what time is it",
            "what's the date",
            "what's the time",
            "what's the current date",
            "what's the current time",
            "what's the current date and time",
            "what day is it",
            "today's date",
            "what is today's date",
            "today date",
            "today"
        }:

            return Intent(
                IntentType.DATETIME
            )

        # =================================================
        # SYSTEM INFO
        # =================================================

        system_info_commands = {
            "system info",
            "system information",
            "computer info",
            "computer information",
            "pc info",
            "pc information",
            "my system info",
            "my system information",
            "what is my system info",
            "what is my system information",
            "what's my system info",
            "what's my system information",
            "show system info",
            "show system information",
            "show computer info",
            "show computer information",
            "show pc info",
            "show pc information"
        }

        if lower in system_info_commands:

            return Intent(
                IntentType.SYSTEM_INFO
            )

        # =================================================
        # WEB SEARCH
        # =================================================

        if lower in {
            "search",
            "web search",
            "search the web",
            "search the internet",
            "google"
        }:

            return Intent(
                IntentType.UNKNOWN
            )

        search_prefixes = [
            "search for ",
            "search the web for ",
            "search the internet for ",
            "web search for ",
            "look up ",
            "look this up ",
            "find this on the web ",
            "google "
        ]

        for prefix in search_prefixes:

            if lower.startswith(prefix):

                query = text[
                    len(prefix):
                ].strip()

                if not query:

                    return Intent(
                        IntentType.UNKNOWN
                    )

                return Intent(
                    IntentType.WEB_SEARCH,
                    query
                )

        # =================================================
        # APPLICATION LAUNCHER
        # =================================================

        application_prefixes = [
            "open ",
            "launch ",
            "start "
        ]

        if lower in {
            "open",
            "launch",
            "start"
        }:

            return Intent(
                IntentType.UNKNOWN
            )

        for prefix in application_prefixes:

            if lower.startswith(prefix):

                application = text[
                    len(prefix):
                ].strip()

                if not application:

                    return Intent(
                        IntentType.UNKNOWN
                    )

                return Intent(
                    IntentType.APPLICATION_LAUNCH,
                    application
                )

        # =================================================
        # AI STATUS
        # =================================================

        if lower == "ai":

            return Intent(
                IntentType.AI_STATUS
            )

        # =================================================
        # EXPLICIT ASK
        # =================================================

        if lower == "ask":

            return Intent(
                IntentType.UNKNOWN
            )

        if lower.startswith("ask "):

            prompt = text[4:].strip()

            if not prompt:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.AI,
                prompt
            )

        # =================================================
        # MEMORY STATUS
        # =================================================

        if lower == "memory":

            return Intent(
                IntentType.MEMORY_STATUS
            )

        if lower == "memory short":

            return Intent(
                IntentType.MEMORY_SHORT
            )

        if lower == "memory long":

            return Intent(
                IntentType.MEMORY_LONG
            )

        if lower == "memory clear short":

            return Intent(
                IntentType.MEMORY_CLEAR_SHORT
            )

        if lower == "memory clear long":

            return Intent(
                IntentType.MEMORY_CLEAR_LONG
            )

        # =================================================
        # MEMORY CATEGORY
        # =================================================

        if lower.startswith(
            "memory category "
        ):

            category = text[
                len("memory category "):
            ].strip()

            if not category:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.MEMORY_CATEGORY,
                category
            )

        # =================================================
        # REMEMBER
        # =================================================

        if lower == "remember":
            return Intent(
                IntentType.MEMORY_REMEMBER,
                ""
            )

        if lower.startswith("remember "):

            content = text[9:].strip()

            if not content:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.MEMORY_REMEMBER,
                content
            )

        # =================================================
        # RECALL
        # =================================================

        if lower == "recall":
            return Intent(
                IntentType.MEMORY_RECALL,
                ""
            )

        if lower.startswith("recall "):

            query = text[7:].strip()

            if not query:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.MEMORY_RECALL,
                query
            )

        # =================================================
        # FORGET
        # =================================================

        if lower == "forget":
            return Intent(
                IntentType.MEMORY_FORGET,
                ""
            )

        if lower.startswith("forget "):

            query = text[7:].strip()

            if not query:
                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.MEMORY_FORGET,
                query
            )

        # =================================================
        # CONVERSATION
        # =================================================

        if lower == "conversation":

            return Intent(
                IntentType.CONVERSATION_STATUS
            )

        if lower == "conversation clear":

            return Intent(
                IntentType.CONVERSATION_CLEAR
            )

        # =================================================
        # PROFILE
        # =================================================

        if lower in {
            "profile",
            "profile status"
        }:

            return Intent(
                IntentType.PROFILE_STATUS
            )

        if lower.startswith("profile set "):

            profile_data = text[
                len("profile set "):
            ].strip()

            if not profile_data:

                return Intent(
                    IntentType.UNKNOWN
                )

            parts = profile_data.split(
                maxsplit=1
            )

            if len(parts) != 2:

                return Intent(
                    IntentType.UNKNOWN
                )

            key = parts[0].strip()

            value = parts[1].strip()

            if not key or not value:

                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.PROFILE_SET,
                {
                    "key": key,
                    "value": value
                }
            )

        if lower == "profile clear":

            return Intent(
                IntentType.PROFILE_CLEAR
            )

        # =================================================
        # NATURAL-LANGUAGE MULTI-STEP CALCULATION
        # =================================================

        multi_step_calculation_markers = [
            "first calculate ",
            "then calculate ",
            "calculate ",
            "take that result",
            "divide by ",
            "add ",
            "subtract ",
            "multiply by ",
            "increase by ",
            "decrease by "
        ]

        if (
                any(
                    marker in lower
                    for marker in multi_step_calculation_markers
                )
                and (
                "then " in lower
                or "first " in lower
                or "step" in lower
                or "each " in lower
                or "result" in lower
        )
        ):
            return Intent(
                IntentType.AGENT,
                text
            )

        # =================================================
        # AGENT
        # =================================================

        if lower == "agent":
            return Intent(
                IntentType.UNKNOWN
            )

        if lower.startswith("agent "):

            request = text[
                len("agent "):
            ].strip()

            if not request:
                return Intent(
                    IntentType.UNKNOWN
                )

            return Intent(
                IntentType.AGENT,
                request
            )

        # =================================================
        # NATURAL-LANGUAGE AGENT REQUEST
        # =================================================

        agent_prefixes = [
            "use the calculator tool ",
            "use calculator tool ",
            "use the python tool ",
            "use python tool ",
            "use the file tool ",
            "use file tool ",
            "use the web search tool ",
            "use web search tool ",
            "use the application launcher ",
            "use application launcher "
        ]

        for prefix in agent_prefixes:

            if lower.startswith(prefix):

                request = text

                if not request.strip():
                    return Intent(
                        IntentType.UNKNOWN
                    )

                return Intent(
                    IntentType.AGENT,
                    request
                )

        # =================================================
        # NORMAL AI REQUEST
        # =================================================

        return Intent(
            IntentType.AI,
            text
        )