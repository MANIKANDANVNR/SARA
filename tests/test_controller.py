from core.controller import SaraController

from memory.conversation_manager import (
    ConversationManager
)

from tools.tool_registry import (
    ToolRegistry
)


# =================================================
# MOCK OBJECTS
# =================================================


class MockSara:

    version = "0.9.0"


class MockState:

    authenticated = True
    running = True


class MockSecurity:

    class MockAudit:

        def record(
            self,
            event,
            action,
            resource,
            result
        ):

            pass

    audit = MockAudit()

    def revoke_all_permissions(self):

        pass


class MockMemory:

    def __init__(self):

        self.short_term = []

        self.long_term = []

        self.long_term_memory = self.long_term

    def remember_short_term(self, content):

        self.short_term.append(
            {
                "content": content
            }
        )

        return True

    def clear_short_term(self):

        self.short_term.clear()

    def clear_long_term(self):

        self.long_term.clear()

    def get_short_term(self):

        return list(self.short_term)

    def get_long_term(self):

        return list(self.long_term)

    def delete_long_term(self, index):

        if (
            index < 0
            or index >= len(self.long_term)
        ):
            return False

        self.long_term.pop(index)

        return True

    def search_long_term(self, query):

        if not query:
            return []

        query = str(query).strip().lower()

        if not query:
            return []

        query_words = set(
            query.split()
        )

        results = []

        for memory in self.long_term:

            content = (
                memory
                .get("content", "")
                .lower()
            )

            category = (
                memory
                .get("category", "general")
                .lower()
            )

            content_words = set(
                content.split()
            )

            exact_match = (
                query in content
                or query in category
            )

            word_match = bool(
                query_words
                & content_words
            )

            if exact_match or word_match:
                results.append(memory)

        return results

    def search_by_category(self, category):

        return []

    def count_short_term(self):

        return len(self.short_term)

    def count_long_term(self):

        return len(self.long_term)

    def remember_long_term(
        self,
        content,
        category="general"
    ):

        self.long_term.append(
            {
                "content": content,
                "category": category
            }
        )

        return True


class MockContext:

    def format_context(self, query):

        return (
            f"Context for: {query}"
        )


class MockBrain:

    available = True

    def __init__(self):

        self.last_prompt = None

        self.last_context = None

    def think(
        self,
        prompt,
        context=None
    ):

        self.last_prompt = prompt

        self.last_context = context

        return "AI response"

    def status(self):

        return {
            "available": True,
            "provider": "mock",
            "model": "mock-model",
            "last_error": None
        }


class MockMemoryStore:

    def __init__(self):

        self.saved_data = None

    def load(self):

        return []

    def save(self, memories):

        self.saved_data = memories

        return True


class MockConversationStore:

    def __init__(self):

        self.saved_messages = None

    def load(self):

        return []

    def save(self, messages):

        self.saved_messages = messages

        return True


class MockProfile:

    def __init__(self):

        self.data = {}

    def set(self, key, value):

        if not key or value is None:

            return False

        key = str(key).strip().lower()

        if not key:

            return False

        self.data[key] = value

        return True

    def load(self, data):

        if isinstance(data, dict):

            self.data = dict(data)

        else:

            self.data = {}

    def get_all(self):

        return dict(self.data)

    def clear(self):

        self.data.clear()


class MockProfileStore:

    def __init__(self):

        self.saved_profile = None

    def load(self):

        return {}

    def save(self, profile):

        self.saved_profile = profile

        return True


class MockTool:

    description = "Mock tool"


# =================================================
# CONTROLLER FACTORY
# =================================================


def create_controller(brain):

    return SaraController(
        sara=MockSara(),
        state=MockState(),
        security=MockSecurity(),
        brain=brain,
        memory=MockMemory(),
        context=MockContext(),
        conversation=ConversationManager(),
        memory_store=MockMemoryStore(),
        conversation_store=MockConversationStore(),
        profile=MockProfile(),
        profile_store=MockProfileStore(),
        tools=ToolRegistry(),
        voice=None,
        ui=None
    )


# =================================================
# AI TESTS
# =================================================


def test_normal_message_routes_to_ai_brain():

    brain = MockBrain()

    controller = create_controller(brain)

    response = controller.handle_command(
        "What is Python?"
    )

    assert response == "AI response"

    assert (
        brain.last_prompt
        == "What is Python?"
    )


def test_explicit_ask_routes_to_ai_brain():

    brain = MockBrain()

    controller = create_controller(brain)

    response = controller.handle_command(
        "ask Explain Python"
    )

    assert response == "AI response"

    assert (
        brain.last_prompt
        == "Explain Python"
    )


def test_normal_message_is_not_legacy_sara_command():

    brain = MockBrain()

    controller = create_controller(brain)

    response = controller.handle_command(
        "Hello SARA"
    )

    assert response == "AI response"

    assert (
        brain.last_prompt
        == "Hello SARA"
    )


def test_ai_status_routes_correctly():

    brain = MockBrain()

    controller = create_controller(brain)

    response = controller.handle_command(
        "ai"
    )

    assert "AI STATUS" in response

    assert "Status: READY" in response

    assert "Provider: mock" in response

    assert "Model: mock-model" in response


# =================================================
# SARA 0.7.0 CONVERSATION TESTS
# =================================================


def test_conversation_is_recorded():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.handle_command(
        "What is Python?"
    )

    controller.handle_command(
        "What is it used for?"
    )

    messages = (
        controller.conversation
        .get_messages()
    )

    assert len(messages) == 4

    assert (
        messages[0]["role"]
        == "user"
    )

    assert (
        messages[0]["content"]
        == "What is Python?"
    )

    assert (
        messages[1]["role"]
        == "assistant"
    )

    assert (
        messages[1]["content"]
        == "AI response"
    )

    assert (
        messages[2]["role"]
        == "user"
    )

    assert (
        messages[2]["content"]
        == "What is it used for?"
    )

    assert (
        messages[3]["role"]
        == "assistant"
    )


def test_conversation_status():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.handle_command(
        "What is Python?"
    )

    response = controller.handle_command(
        "conversation"
    )

    assert (
        "CONVERSATION STATUS"
        in response
    )

    assert "Messages: 2" in response

    assert "Maximum messages: 20" in response

    assert "Persistent history: ACTIVE" in response


def test_conversation_clear():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.handle_command(
        "Hello SARA"
    )

    assert (
        controller.conversation
        .message_count()
        == 2
    )

    response = controller.handle_command(
        "conversation clear"
    )

    assert (
        response
        == "Conversation history cleared."
    )

    assert (
        controller.conversation
        .message_count()
        == 0
    )


def test_conversation_is_separate_from_short_term_memory():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.handle_command(
        "Hello SARA"
    )

    conversation_count = (
        controller.conversation
        .message_count()
    )

    memory_count = (
        controller.memory
        .count_short_term()
    )

    assert conversation_count == 2

    assert memory_count == 2


# =================================================
# AI CONTEXT TEST
# =================================================


def test_ai_receives_context():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.handle_command(
        "What is Python?"
    )

    assert (
        brain.last_context
        == "Context for: What is Python?"
    )


def test_controller_passes_conversation_context_to_ai():

    from memory.memory_manager import (
        MemoryManager
    )

    from memory.context_manager import (
        ContextManager
    )

    brain = MockBrain()

    controller = create_controller(
        brain
    )

    controller.memory = MemoryManager()

    controller.context = ContextManager(
        memory_manager=controller.memory,
        conversation_manager=controller.conversation
    )

    controller.conversation.add_user_message(
        "My name is Mani."
    )

    controller.conversation.add_assistant_message(
        "Nice to meet you, Mani."
    )

    response = controller.handle_command(
        "ask What is my name?"
    )

    assert response == "AI response"

    assert (
        brain.last_prompt
        == "What is my name?"
    )

    assert (
        "Current conversation:"
        in brain.last_context
    )

    assert (
        "User: My name is Mani."
        in brain.last_context
    )

    assert (
        "SARA: Nice to meet you, Mani."
        in brain.last_context
    )

    assert (
        "User: What is my name?"
        in brain.last_context
    )


# =================================================
# SARA 0.7.0 PERSISTENCE TESTS
# =================================================


def test_controller_saves_conversation_after_ai_response():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.handle_command(
        "Hello SARA"
    )

    saved = (
        controller
        .conversation_store
        .saved_messages
    )

    assert saved is not None

    assert len(saved) == 2


def test_controller_load_persistent_data():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.memory_store.load = (
        lambda: [
            {
                "content": "My name is Mani.",
                "category": "personal"
            }
        ]
    )

    controller.conversation_store.load = (
        lambda: [
            {
                "role": "user",
                "content": "Hello SARA"
            },
            {
                "role": "assistant",
                "content": "Hello Mani."
            }
        ]
    )

    controller.profile_store.load = (
        lambda: {
            "name": "Mani"
        }
    )

    controller.load_persistent_data()

    assert (
        controller.memory.long_term_memory
        == [
            {
                "content": "My name is Mani.",
                "category": "personal"
            }
        ]
    )

    assert (
        controller.conversation.get_messages()
        == [
            {
                "role": "user",
                "content": "Hello SARA"
            },
            {
                "role": "assistant",
                "content": "Hello Mani."
            }
        ]
    )

    assert (
        controller.profile.get_all()
        == {
            "name": "Mani"
        }
    )


# =================================================
# AUTOMATIC MEMORY TESTS
# =================================================


def test_automatic_memory_requires_authentication():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = False

    result = controller.save_automatic_memory(
        "I am learning Python."
    )

    assert result is False

    assert (
        controller.memory.count_long_term()
        == 0
    )


def test_automatic_memory_saves_important_information():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    result = controller.save_automatic_memory(
        "I am learning Python."
    )

    assert result is True

    memories = (
        controller.memory.get_long_term()
    )

    assert len(memories) == 1

    assert (
        memories[0]["content"]
        == "I am learning Python."
    )

    assert (
        memories[0]["category"]
        == "technical"
    )


def test_automatic_memory_ignores_normal_message():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    result = controller.save_automatic_memory(
        "What is Python?"
    )

    assert result is False

    assert (
        controller.memory.count_long_term()
        == 0
    )


def test_automatic_memory_prevents_duplicates():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    first_result = (
        controller.save_automatic_memory(
            "I am learning Python."
        )
    )

    second_result = (
        controller.save_automatic_memory(
            "I am learning Python."
        )
    )

    assert first_result is True

    assert second_result is False

    assert (
        controller.memory.count_long_term()
        == 1
    )


def test_automatic_memory_saves_to_persistent_store():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    result = controller.save_automatic_memory(
        "I am building SARA."
    )

    assert result is True

    assert (
        controller.memory_store.saved_data
        is not None
    )

    assert (
        len(
            controller.memory_store.saved_data
        )
        == 1
    )

    assert (
        controller.memory_store.saved_data[0][
            "content"
        ]
        == "I am building SARA."
    )

    assert (
        controller.memory_store.saved_data[0][
            "category"
        ]
        == "projects"
    )


def test_ai_automatically_saves_important_memory():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    response = controller.handle_command(
        "I am learning Python."
    )

    assert response == "AI response"

    memories = (
        controller.memory.get_long_term()
    )

    assert len(memories) == 1

    assert (
        memories[0]["content"]
        == "I am learning Python."
    )

    assert (
        memories[0]["category"]
        == "technical"
    )


def test_ai_does_not_automatically_save_normal_message():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    response = controller.handle_command(
        "What is Python?"
    )

    assert response == "AI response"

    assert (
        controller.memory.count_long_term()
        == 0
    )


def test_ai_does_not_save_automatic_memory_when_logged_out():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = False

    response = controller.handle_command(
        "I am learning Python."
    )

    assert response == "AI response"

    assert (
        controller.memory.count_long_term()
        == 0
    )


def test_ai_automatic_memory_prevents_duplicate():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    controller.handle_command(
        "I am learning Python."
    )

    controller.handle_command(
        "I am learning Python."
    )

    assert (
        controller.memory.count_long_term()
        == 1
    )


# =================================================
# EXPLICIT LONG-TERM MEMORY TESTS
# =================================================


def test_remember_long_term_saves_new_memory():

    brain = MockBrain()

    controller = create_controller(brain)

    response = controller.remember_long_term(
        "My favorite programming language is Python."
    )

    assert (
        response
        == (
            "I will remember that "
            "under preferences memory."
        )
    )

    assert (
        len(
            controller.memory.get_long_term()
        )
        == 1
    )

    assert (
        controller.memory.get_long_term()[0][
            "content"
        ]
        == (
            "My favorite programming language "
            "is Python."
        )
    )


def test_remember_long_term_rejects_duplicate_memory():

    brain = MockBrain()

    controller = create_controller(brain)

    first_response = (
        controller.remember_long_term(
            "My favorite programming language "
            "is Python."
        )
    )

    second_response = (
        controller.remember_long_term(
            "My favorite programming language "
            "is Python."
        )
    )

    assert (
        first_response
        == (
            "I will remember that "
            "under preferences memory."
        )
    )

    assert (
        second_response
        == "That memory already exists."
    )

    assert (
        len(
            controller.memory.get_long_term()
        )
        == 1
    )


def test_remember_long_term_duplicate_check_is_case_insensitive():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.remember_long_term(
        "My favorite programming language "
        "is Python."
    )

    response = (
        controller.remember_long_term(
            "my FAVORITE programming language "
            "is PYTHON."
        )
    )

    assert (
        response
        == "That memory already exists."
    )

    assert (
        len(
            controller.memory.get_long_term()
        )
        == 1
    )


def test_remember_long_term_duplicate_check_ignores_outer_whitespace():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.remember_long_term(
        "My favorite programming language "
        "is Python."
    )

    response = (
        controller.remember_long_term(
            "   My favorite programming language "
            "is Python.   "
        )
    )

    assert (
        response
        == "That memory already exists."
    )

    assert (
        len(
            controller.memory.get_long_term()
        )
        == 1
    )


# =================================================
# MEMORY FORGET TESTS
# =================================================


def test_memory_forget_requires_authentication():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = False

    controller.memory.remember_long_term(
        "My favorite programming language is Python.",
        "preferences"
    )

    response = controller.forget(
        "favorite programming language"
    )

    assert (
        response
        == (
            "Permission denied. "
            "Authentication required "
            "to forget long-term memory."
        )
    )

    assert (
        controller.memory.count_long_term()
        == 1
    )


def test_memory_forget_rejects_empty_query():

    brain = MockBrain()

    controller = create_controller(brain)

    response = controller.forget("")

    assert (
        response
        == "Memory query cannot be empty."
    )


def test_memory_forget_handles_no_match():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.memory.remember_long_term(
        "My favorite programming language is Python.",
        "preferences"
    )

    response = controller.forget(
        "JavaScript database"
    )

    assert (
        response
        == (
            "I couldn't find any memory "
            "matching that request."
        )
    )

    assert (
        controller.memory.count_long_term()
        == 1
    )


def test_memory_forget_deletes_exact_match():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.memory.remember_long_term(
        "My favorite programming language is Python.",
        "preferences"
    )

    controller.memory.remember_long_term(
        "I am building SARA.",
        "projects"
    )

    response = controller.forget(
        "favorite programming language"
    )

    assert (
        response
        == (
            "I have forgotten that memory: "
            "My favorite programming language is Python."
        )
    )

    memories = (
        controller.memory.get_long_term()
    )

    assert len(memories) == 1

    assert (
        memories[0]["content"]
        == "I am building SARA."
    )


def test_memory_forget_persists_deletion():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.memory.remember_long_term(
        "My favorite programming language is Python.",
        "preferences"
    )

    controller.forget(
        "favorite programming language"
    )

    assert (
        controller.memory_store.saved_data
        == []
    )


def test_memory_forget_records_audit_event():

    class AuditRecorder:

        def __init__(self):

            self.events = []

        def record(
            self,
            event,
            action,
            resource,
            result
        ):

            self.events.append(
                {
                    "event": event,
                    "action": action,
                    "resource": resource,
                    "result": result
                }
            )

    brain = MockBrain()

    controller = create_controller(brain)

    audit = AuditRecorder()

    controller.security.audit = audit

    controller.memory.remember_long_term(
        "My favorite programming language is Python.",
        "preferences"
    )

    controller.forget(
        "favorite programming language"
    )

    assert (
        audit.events[-1]
        == {
            "event": "MEMORY_FORGOTTEN",
            "action": "forget",
            "resource": "long_term_memory",
            "result": "success"
        }
    )


# =================================================
# PROFILE TESTS
# =================================================


def test_profile_set_requires_authentication():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = False

    response = controller.handle_command(
        "profile set name Mani"
    )

    assert (
        response
        == "Permission denied. Authentication required."
    )

    assert (
        controller.profile.get_all()
        == {}
    )


def test_profile_set_updates_profile():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    response = controller.handle_command(
        "profile set name Mani"
    )

    assert (
        response
        == "Profile updated: name = Mani"
    )

    assert (
        controller.profile.get_all()
        == {
            "name": "Mani"
        }
    )


def test_profile_set_saves_profile():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.state.authenticated = True

    controller.handle_command(
        "profile set name Mani"
    )

    assert (
        controller.profile_store.saved_profile
        == {
            "name": "Mani"
        }
    )


# =================================================
# SARA 0.8.0 TOOL REGISTRY TESTS
# =================================================


def test_controller_registers_tool():

    brain = MockBrain()

    controller = create_controller(brain)

    tool = MockTool()

    result = controller.register_tool(
        "calculator",
        tool
    )

    assert result is True

    assert controller.tool_exists(
        "calculator"
    )

    assert controller.get_tool(
        "calculator"
    ) is tool


def test_controller_get_tool_returns_none_for_unknown_tool():

    brain = MockBrain()

    controller = create_controller(brain)

    assert controller.get_tool(
        "unknown"
    ) is None


def test_controller_lists_registered_tools():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.register_tool(
        "python",
        MockTool()
    )

    assert controller.list_tools() == [
        "calculator",
        "python"
    ]


def test_controller_counts_registered_tools():

    brain = MockBrain()

    controller = create_controller(brain)

    assert controller.tool_count() == 0

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.register_tool(
        "python",
        MockTool()
    )

    assert controller.tool_count() == 2


def test_controller_returns_tool_definitions():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.register_tool(
        "calculator",
        MockTool()
    )

    definitions = (
        controller.tool_definitions()
    )

    assert definitions == [
        {
            "name": "calculator",
            "description": "Mock tool"
        }
    ]


def test_ai_status_reports_tools_enabled():

    brain = MockBrain()

    controller = create_controller(brain)

    controller.register_tool(
        "calculator",
        MockTool()
    )

    response = controller.handle_command(
        "ai"
    )

    assert (
        "Tools enabled: True"
        in response
    )


# =================================================
# SARA 0.8.0 SECURITY GATE TESTS
# =================================================

from core.state import SaraState

from security.security_manager import (
    SecurityManager
)

from security.permission import (
    PermissionType,
    PermissionLevel
)


class SecureMockSara:

    version = "0.8.0"


class SecureMockBrain:

    available = True

    def think(
        self,
        prompt,
        context=None
    ):

        return "AI response"

    def status(self):

        return {
            "available": True,
            "provider": "mock",
            "model": "mock-model",
            "last_error": None
        }


def create_secure_controller():

    state = SaraState()

    security = SecurityManager(
        state
    )

    return SaraController(
        sara=SecureMockSara(),
        state=state,
        security=security,
        brain=SecureMockBrain(),
        memory=MockMemory(),
        context=MockContext(),
        conversation=ConversationManager(),
        memory_store=MockMemoryStore(),
        conversation_store=MockConversationStore(),
        profile=MockProfile(),
        profile_store=MockProfileStore(),
        tools=ToolRegistry(),
        voice=None,
        ui=None
    )


def test_controller_tool_authorization_requires_authentication():

    controller = create_secure_controller()

    controller.register_tool(
        "calculator",
        MockTool()
    )

    result = controller.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False


def test_controller_tool_authorization_requires_permission():

    controller = create_secure_controller()

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.security.authenticate()

    result = controller.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False


def test_controller_tool_authorization_allows_valid_permission():

    controller = create_secure_controller()

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.security.authenticate()

    controller.security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    result = controller.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is True


def test_controller_tool_access_request():

    controller = create_secure_controller()

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.security.authenticate()

    result = controller.request_tool_access(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW,
        duration=60
    )

    assert result is True


def test_controller_cannot_authorize_unknown_tool():

    controller = create_secure_controller()

    controller.security.authenticate()

    controller.security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    result = controller.authorize_tool(
        tool_name="unknown",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False


def test_controller_tool_access_is_blocked_after_logout():

    controller = create_secure_controller()

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.security.authenticate()

    controller.security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    controller.security.logout()

    result = controller.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False


def test_controller_tool_access_is_blocked_after_emergency_shutdown():

    controller = create_secure_controller()

    controller.register_tool(
        "calculator",
        MockTool()
    )

    controller.security.authenticate()

    controller.security.request_permission(
        PermissionType.SYSTEM,
        PermissionLevel.LOW,
        duration=60
    )

    controller.security.emergency_shutdown()

    result = controller.authorize_tool(
        tool_name="calculator",
        permission_type=PermissionType.SYSTEM,
        level=PermissionLevel.LOW
    )

    assert result is False