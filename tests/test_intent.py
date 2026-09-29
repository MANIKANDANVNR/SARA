from core.intent import (
    IntentRouter,
    IntentType
)


def test_normal_message_routes_to_ai():

    router = IntentRouter()

    intent = router.route(
        "What is Python?"
    )

    assert intent.type == IntentType.AI

    assert (
        intent.value
        == "What is Python?"
    )


def test_ask_command_routes_to_ai():

    router = IntentRouter()

    intent = router.route(
        "ask What is Python?"
    )

    assert intent.type == IntentType.AI

    assert (
        intent.value
        == "What is Python?"
    )


def test_ai_status():

    router = IntentRouter()

    intent = router.route("ai")

    assert (
        intent.type
        == IntentType.AI_STATUS
    )


def test_memory_status():

    router = IntentRouter()

    intent = router.route("memory")

    assert (
        intent.type
        == IntentType.MEMORY_STATUS
    )


def test_memory_short():

    router = IntentRouter()

    intent = router.route(
        "memory short"
    )

    assert (
        intent.type
        == IntentType.MEMORY_SHORT
    )


def test_memory_long():

    router = IntentRouter()

    intent = router.route(
        "memory long"
    )

    assert (
        intent.type
        == IntentType.MEMORY_LONG
    )


def test_clear_short_memory():

    router = IntentRouter()

    intent = router.route(
        "memory clear short"
    )

    assert (
        intent.type
        == IntentType.MEMORY_CLEAR_SHORT
    )


def test_clear_long_memory():

    router = IntentRouter()

    intent = router.route(
        "memory clear long"
    )

    assert (
        intent.type
        == IntentType.MEMORY_CLEAR_LONG
    )


def test_remember_command():

    router = IntentRouter()

    intent = router.route(
        "remember I like Python"
    )

    assert (
        intent.type
        == IntentType.MEMORY_REMEMBER
    )

    assert (
        intent.value
        == "I like Python"
    )


def test_recall_command():

    router = IntentRouter()

    intent = router.route(
        "recall Python"
    )

    assert (
        intent.type
        == IntentType.MEMORY_RECALL
    )

    assert (
        intent.value
        == "Python"
    )


def test_shutdown_commands():

    router = IntentRouter()

    for command in [
        "shutdown",
        "exit",
        "quit"
    ]:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.SHUTDOWN
        )


def test_empty_command():

    router = IntentRouter()

    intent = router.route("")

    assert (
        intent.type
        == IntentType.UNKNOWN
    )


def test_whitespace_command():

    router = IntentRouter()

    intent = router.route("   ")

    assert (
        intent.type
        == IntentType.UNKNOWN
    )


def test_case_insensitive_commands():

    router = IntentRouter()

    intent = router.route(
        "SHUTDOWN"
    )

    assert (
        intent.type
        == IntentType.SHUTDOWN
    )


def test_empty_ask_command():

    router = IntentRouter()

    intent = router.route("ask")

    assert intent.type == IntentType.UNKNOWN


def test_empty_remember_command():
    router = IntentRouter()

    intent = router.route(
        "remember"
    )

    assert (
        intent.type
        == IntentType.MEMORY_REMEMBER
    )

    assert intent.value == ""


def test_empty_recall_command():
    router = IntentRouter()

    intent = router.route(
        "recall"
    )

    assert (
        intent.type
        == IntentType.MEMORY_RECALL
    )

    assert intent.value == ""


# =================================================
# SARA 0.6.0 CONVERSATION TESTS
# =================================================


def test_conversation_status():

    router = IntentRouter()

    intent = router.route(
        "conversation"
    )

    assert (
        intent.type
        == IntentType.CONVERSATION_STATUS
    )


def test_conversation_clear():

    router = IntentRouter()

    intent = router.route(
        "conversation clear"
    )

    assert (
        intent.type
        == IntentType.CONVERSATION_CLEAR
    )


def test_conversation_commands_case_insensitive():

    router = IntentRouter()

    status = router.route(
        "CONVERSATION"
    )

    clear = router.route(
        "CONVERSATION CLEAR"
    )

    assert (
        status.type
        == IntentType.CONVERSATION_STATUS
    )

    assert (
        clear.type
        == IntentType.CONVERSATION_CLEAR
    )


# =================================================
# SARA 0.8.0 CALCULATOR TESTS
# =================================================


def test_calculate_command_routes_to_calculator():

    router = IntentRouter()

    intent = router.route(
        "calculate 25 * 8"
    )

    assert (
        intent.type
        == IntentType.CALCULATOR
    )

    assert (
        intent.value
        == "25 * 8"
    )


def test_calculate_command_preserves_expression():

    router = IntentRouter()

    intent = router.route(
        "calculate (100 + 50) / 5"
    )

    assert (
        intent.type
        == IntentType.CALCULATOR
    )

    assert (
        intent.value
        == "(100 + 50) / 5"
    )


def test_calculate_command_is_case_insensitive():

    router = IntentRouter()

    intent = router.route(
        "CALCULATE 10 * 5"
    )

    assert (
        intent.type
        == IntentType.CALCULATOR
    )

    assert (
        intent.value
        == "10 * 5"
    )


def test_calculate_without_expression_is_unknown():

    router = IntentRouter()

    intent = router.route(
        "calculate"
    )

    assert (
        intent.type
        == IntentType.UNKNOWN
    )


def test_calculator_does_not_capture_normal_ai_request():

    router = IntentRouter()

    intent = router.route(
        "Can you calculate my career options?"
    )

    assert (
        intent.type
        == IntentType.AI
    )


# =================================================
# SARA 0.8.0 PYTHON TESTS
# =================================================


def test_python_command_routes_to_python():

    router = IntentRouter()

    intent = router.route(
        "python 10 + 20"
    )

    assert (
        intent.type
        == IntentType.PYTHON
    )

    assert (
        intent.value
        == "10 + 20"
    )


def test_python_command_preserves_code():

    router = IntentRouter()

    intent = router.route(
        "python print(25 * 4)"
    )

    assert (
        intent.type
        == IntentType.PYTHON
    )

    assert (
        intent.value
        == "print(25 * 4)"
    )


def test_python_command_is_case_insensitive():

    router = IntentRouter()

    intent = router.route(
        "PYTHON 10 + 5"
    )

    assert (
        intent.type
        == IntentType.PYTHON
    )

    assert (
        intent.value
        == "10 + 5"
    )


def test_python_without_code_is_unknown():

    router = IntentRouter()

    intent = router.route(
        "python"
    )

    assert (
        intent.type
        == IntentType.UNKNOWN
    )


def test_python_does_not_capture_normal_ai_request():

    router = IntentRouter()

    intent = router.route(
        "Can you explain Python?"
    )

    assert (
        intent.type
        == IntentType.AI
    )


# =================================================
# SARA 0.8.0 FILE WRITE TESTS
# =================================================


def test_file_write_intent():

    router = IntentRouter()

    result = router.route(
        "write file C:\\test.txt Hello SARA"
    )

    assert result.type == (
        IntentType.FILE_WRITE
    )

    assert result.value == {
        "path": "C:\\test.txt",
        "content": "Hello SARA"
    }


def test_file_write_intent_with_spaces_in_content():

    router = IntentRouter()

    result = router.route(
        "write file C:\\test.txt Hello SARA this is a test"
    )

    assert result.type == (
        IntentType.FILE_WRITE
    )

    assert result.value == {
        "path": "C:\\test.txt",
        "content": "Hello SARA this is a test"
    }


def test_file_write_intent_empty_command():

    router = IntentRouter()

    result = router.route(
        "write file"
    )

    assert result.type == (
        IntentType.UNKNOWN
    )


def test_file_write_intent_missing_content():

    router = IntentRouter()

    result = router.route(
        "write file C:\\test.txt"
    )

    assert result.type == (
        IntentType.UNKNOWN
    )


def test_file_write_intent_is_case_insensitive():

    router = IntentRouter()

    result = router.route(
        "WRITE FILE C:\\test.txt Hello SARA"
    )

    assert result.type == (
        IntentType.FILE_WRITE
    )

    assert result.value == {
        "path": "C:\\test.txt",
        "content": "Hello SARA"
    }


def test_file_write_intent_preserves_content_case():

    router = IntentRouter()

    result = router.route(
        "write file C:\\test.txt Hello SARA"
    )

    assert result.value["content"] == (
        "Hello SARA"
    )


def test_file_write_intent_with_unix_style_path():

    router = IntentRouter()

    result = router.route(
        "write file /tmp/test.txt Hello SARA"
    )

    assert result.type == (
        IntentType.FILE_WRITE
    )

    assert result.value == {
        "path": "/tmp/test.txt",
        "content": "Hello SARA"
    }


def test_file_write_intent_requires_path_and_content():

    router = IntentRouter()

    result = router.route(
        "write file Hello"
    )

    assert result.type == (
        IntentType.UNKNOWN
    )


# =================================================
# SARA 0.8.0 DATE & TIME TESTS
# =================================================


def test_date_time_command_routes_to_datetime():

    router = IntentRouter()

    for command in [
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
        "what's the date",
        "what's the time",
        "what's the current date",
        "what's the current time",
        "what's the current date and time",
        "what day is it",
        "today's date",
        "today date",
        "today"
    ]:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.DATETIME
        )


def test_date_time_command_is_case_insensitive():

    router = IntentRouter()

    for command in [
        "DATE",
        "TIME",
        "CURRENT DATE",
        "WHAT IS THE DATE",
        "WHAT IS THE CURRENT TIME",
        "TODAY"
    ]:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.DATETIME
        )


def test_date_time_command_has_no_value():

    router = IntentRouter()

    intent = router.route(
        "current date and time"
    )

    assert (
        intent.type
        == IntentType.DATETIME
    )

    assert intent.value is None


def test_datetime_does_not_capture_normal_ai_request():

    router = IntentRouter()

    for command in [
        "Can you explain today's date?",
        "What is the current time in Tokyo?",
        "Tell me what time means",
        "I want to know today's date"
    ]:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.AI
        )


# =================================================
# SARA 0.8.0 WEB SEARCH TESTS
# =================================================


def test_web_search_command_routes_to_web_search():

    router = IntentRouter()

    intent = router.route(
        "search for Python developer jobs"
    )

    assert (
        intent.type
        == IntentType.WEB_SEARCH
    )

    assert (
        intent.value
        == "Python developer jobs"
    )


def test_web_search_preserves_query_case():

    router = IntentRouter()

    intent = router.route(
        "search for Python Jobs in Tamil Nadu"
    )

    assert (
        intent.type
        == IntentType.WEB_SEARCH
    )

    assert (
        intent.value
        == "Python Jobs in Tamil Nadu"
    )


def test_web_search_command_is_case_insensitive():

    router = IntentRouter()

    intent = router.route(
        "SEARCH FOR Python Developer Jobs"
    )

    assert (
        intent.type
        == IntentType.WEB_SEARCH
    )

    assert (
        intent.value
        == "Python Developer Jobs"
    )


def test_web_search_prefix_variations():

    router = IntentRouter()

    commands = [
        (
            "search the web for Python jobs",
            "Python jobs"
        ),
        (
            "search the internet for Python jobs",
            "Python jobs"
        ),
        (
            "web search for Python jobs",
            "Python jobs"
        ),
        (
            "look up Python jobs",
            "Python jobs"
        ),
        (
            "google Python jobs",
            "Python jobs"
        )
    ]

    for command, expected_query in commands:

        intent = router.route(
            command
        )

        assert (
            intent.type
            == IntentType.WEB_SEARCH
        )

        assert (
            intent.value
            == expected_query
        )


def test_web_search_without_query_is_unknown():

    router = IntentRouter()

    for command in [
        "search",
        "web search",
        "search the web",
        "search the internet",
        "google"
    ]:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.UNKNOWN
        )


def test_web_search_does_not_capture_normal_ai_request():

    router = IntentRouter()

    commands = [
        "Can you search for Python?",
        "I want to search for a job",
        "What is web search?",
        "Can you explain Google?"
    ]

    for command in commands:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.AI
        )


# =================================================
# SARA 0.8.0 APPLICATION LAUNCHER TESTS
# =================================================


def test_application_launch_command_routes_to_launcher():

    router = IntentRouter()

    commands = [
        (
            "open Chrome",
            "Chrome"
        ),
        (
            "launch notepad",
            "notepad"
        ),
        (
            "start calculator",
            "calculator"
        ),
        (
            "open VS Code",
            "VS Code"
        ),
        (
            "open PyCharm",
            "PyCharm"
        )
    ]

    for command, expected_application in commands:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.APPLICATION_LAUNCH
        )

        assert (
            intent.value
            == expected_application
        )


def test_application_launch_command_is_case_insensitive():

    router = IntentRouter()

    intent = router.route(
        "OPEN CHROME"
    )

    assert (
        intent.type
        == IntentType.APPLICATION_LAUNCH
    )

    assert (
        intent.value
        == "CHROME"
    )


def test_application_launch_preserves_application_name():

    router = IntentRouter()

    intent = router.route(
        "open Google Chrome"
    )

    assert (
        intent.type
        == IntentType.APPLICATION_LAUNCH
    )

    assert (
        intent.value
        == "Google Chrome"
    )


def test_application_launch_without_application_is_unknown():

    router = IntentRouter()

    for command in [
        "open",
        "launch",
        "start"
    ]:

        intent = router.route(command)

        assert (
            intent.type
            == IntentType.UNKNOWN
        )

# =================================================
# SARA 0.9.0 AGENT ROUTING TESTS
# =================================================


def test_agent_command_routes_to_agent():

    router = IntentRouter()

    intent = router.route(
        "agent Calculate 157 * 83"
    )

    assert (
        intent.type
        == IntentType.AGENT
    )

    assert (
        intent.value
        == "Calculate 157 * 83"
    )


def test_agent_command_is_case_insensitive():

    router = IntentRouter()

    intent = router.route(
        "AGENT Calculate 157 * 83"
    )

    assert (
        intent.type
        == IntentType.AGENT
    )

    assert (
        intent.value
        == "Calculate 157 * 83"
    )


def test_natural_language_tool_request_routes_to_agent():

    router = IntentRouter()

    intent = router.route(
        "Use the calculator tool to calculate "
        "157 * 83. Return only the result."
    )

    assert (
        intent.type
        == IntentType.AGENT
    )

    assert (
        intent.value
        == (
            "Use the calculator tool to calculate "
            "157 * 83. Return only the result."
        )
    )


def test_normal_ai_request_still_routes_to_ai():

    router = IntentRouter()

    intent = router.route(
        "What is Python?"
    )

    assert (
        intent.type
        == IntentType.AI
    )

    assert (
        intent.value
        == "What is Python?"
    )

# =================================================
# SARA 0.9.0 NATURAL-LANGUAGE CALCULATION TESTS
# =================================================


def test_multi_step_calculation_routes_to_agent():

    router = IntentRouter()

    intent = router.route(
        "Calculate 157 * 83, divide by 7, "
        "add 1234, use appropriate tool each step."
    )

    assert (
        intent.type
        == IntentType.AGENT
    )

    assert (
        intent.value
        == (
            "Calculate 157 * 83, divide by 7, "
            "add 1234, use appropriate tool each step."
        )
    )


def test_sequential_calculation_routes_to_agent():

    router = IntentRouter()

    intent = router.route(
        "First calculate 157 * 83. "
        "Then take that result and divide by 7."
    )

    assert (
        intent.type
        == IntentType.AGENT
    )

    assert (
        intent.value
        == (
            "First calculate 157 * 83. "
            "Then take that result and divide by 7."
        )
    )


def test_compound_calculation_routes_to_agent():

    router = IntentRouter()

    intent = router.route(
        "Calculate compound result starting 10,000, "
        "7.5% increase three times, subtract 1,250. "
        "Exact result and steps."
    )

    assert (
        intent.type
        == IntentType.AGENT
    )

    assert (
        intent.value
        == (
            "Calculate compound result starting 10,000, "
            "7.5% increase three times, subtract 1,250. "
            "Exact result and steps."
        )
    )

# =================================================
# SARA 0.9.0 MEMORY FORGET TESTS
# =================================================


def test_forget_command_routes_to_memory_forget():

    router = IntentRouter()

    intent = router.route(
        "forget my favorite programming language"
    )

    assert (
        intent.type
        == IntentType.MEMORY_FORGET
    )

    assert (
        intent.value
        == "my favorite programming language"
    )


def test_forget_command_is_case_insensitive():

    router = IntentRouter()

    intent = router.route(
        "FORGET Python"
    )

    assert (
        intent.type
        == IntentType.MEMORY_FORGET
    )

    assert (
        intent.value
        == "Python"
    )


def test_empty_forget_command():
    router = IntentRouter()

    intent = router.route(
        "forget"
    )

    assert (
        intent.type
        == IntentType.MEMORY_FORGET
    )

    assert intent.value == ""