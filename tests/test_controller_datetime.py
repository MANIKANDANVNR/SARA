from core.controller import SaraController
from core.state import SaraState
from core.intent import IntentRouter

from security.security_manager import (
    SecurityManager
)


class FakeTool:

    name = "datetime"

    description = (
        "Provides the current local date and time."
    )

    def __init__(self):

        self.called = False

    def execute(self):

        self.called = True

        return {
            "date": "2026-09-13",
            "time": "14:30:00",
            "datetime": "2026-09-13 14:30:00",
            "day": "Sunday"
        }


class FakeTools:

    def __init__(self, tool):

        self.tool = tool

    def get(self, name):

        if name == "datetime":

            return self.tool

        return None

    def exists(self, name):

        return name == "datetime"

    def register(self, name, tool):

        return True

    def list_tools(self):

        return ["datetime"]

    def count(self):

        return 1

    def get_definitions(self):

        return [
            {
                "name": "datetime",
                "description": self.tool.description
            }
        ]


class FakeSara:

    def __init__(self):

        self.intent_router = (
            IntentRouter()
        )


class FakeBrain:

    available = True


class FakeMemory:

    def __init__(self):

        self.long_term_memory = []

    def get_long_term(self):

        return self.long_term_memory


class FakeContext:

    pass


class FakeConversation:

    pass


class FakeStore:

    def load(self):

        return []

    def save(self, data):

        pass


class FakeProfile:

    def get_all(self):

        return {}


class FakeVoice:

    pass


class FakeUI:

    pass


def create_controller():

    state = SaraState()

    security = SecurityManager(
        state
    )

    tool = FakeTool()

    tools = FakeTools(
        tool
    )

    sara = FakeSara()

    controller = SaraController(
        sara=sara,
        state=state,
        security=security,
        brain=FakeBrain(),
        memory=FakeMemory(),
        context=FakeContext(),
        conversation=FakeConversation(),
        memory_store=FakeStore(),
        conversation_store=FakeStore(),
        profile=FakeProfile(),
        profile_store=FakeStore(),
        tools=tools,
        voice=FakeVoice(),
        ui=FakeUI()
    )

    return controller, tool


def test_datetime_command_routes_to_controller():

    controller, tool = (
        create_controller()
    )

    result = controller.handle_command(
        "current date and time"
    )

    assert tool.called is True

    assert "DATE & TIME" in result


def test_datetime_response_contains_date():

    controller, tool = (
        create_controller()
    )

    result = controller.handle_command(
        "date"
    )

    assert (
        "Date: 2026-09-13"
        in result
    )


def test_datetime_response_contains_time():

    controller, tool = (
        create_controller()
    )

    result = controller.handle_command(
        "time"
    )

    assert (
        "Time: 14:30:00"
        in result
    )


def test_datetime_response_contains_day():

    controller, tool = (
        create_controller()
    )

    result = controller.handle_command(
        "what day is it"
    )

    assert (
        "Day: Sunday"
        in result
    )


def test_datetime_does_not_require_authentication():

    controller, tool = (
        create_controller()
    )

    assert (
        controller.state.authenticated
        is False
    )

    result = controller.handle_command(
        "current time"
    )

    assert tool.called is True

    assert (
        "Time: 14:30:00"
        in result
    )


def test_datetime_tool_missing():

    state = SaraState()

    security = SecurityManager(
        state
    )

    class EmptyTools:

        def get(self, name):

            return None

        def exists(self, name):

            return False

        def register(self, name, tool):

            return True

        def list_tools(self):

            return []

        def count(self):

            return 0

        def get_definitions(self):

            return []

    sara = FakeSara()

    controller = SaraController(
        sara=sara,
        state=state,
        security=security,
        brain=FakeBrain(),
        memory=FakeMemory(),
        context=FakeContext(),
        conversation=FakeConversation(),
        memory_store=FakeStore(),
        conversation_store=FakeStore(),
        profile=FakeProfile(),
        profile_store=FakeStore(),
        tools=EmptyTools(),
        voice=FakeVoice(),
        ui=FakeUI()
    )

    result = controller.handle_command(
        "date"
    )

    assert (
        result
        == "Date & Time tool is unavailable."
    )