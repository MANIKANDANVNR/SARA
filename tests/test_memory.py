from memory.memory_manager import (
    MemoryManager
)

from memory.memory_store import (
    MemoryStore
)

from memory.context_manager import (
    ContextManager
)

from memory.conversation_manager import (
    ConversationManager
)

from memory.conversation_store import (
    ConversationStore
)

from memory.profile_manager import (
    ProfileManager
)

from memory.profile_store import (
    ProfileStore
)


# =================================================
# MEMORY MANAGER
# =================================================


def test_short_term_memory():

    memory = MemoryManager(
        max_short_term=3
    )

    assert memory.remember_short_term(
        "Hello"
    )

    assert memory.remember_short_term(
        "How are you?"
    )

    memories = memory.get_short_term()

    assert len(memories) == 2

    assert (
        memories[0]["content"]
        == "Hello"
    )

    assert (
        memories[1]["content"]
        == "How are you?"
    )


def test_short_term_memory_limit():

    memory = MemoryManager(
        max_short_term=2
    )

    memory.remember_short_term("One")

    memory.remember_short_term("Two")

    memory.remember_short_term("Three")

    memories = memory.get_short_term()

    assert len(memories) == 2

    assert (
        memories[0]["content"]
        == "Two"
    )

    assert (
        memories[1]["content"]
        == "Three"
    )


def test_clear_short_term_memory():

    memory = MemoryManager()

    memory.remember_short_term(
        "Temporary memory"
    )

    assert (
        memory.count_short_term()
        == 1
    )

    memory.clear_short_term()

    assert (
        memory.count_short_term()
        == 0
    )


# =================================================
# LONG-TERM MEMORY
# =================================================


def test_long_term_memory():

    memory = MemoryManager()

    assert memory.remember_long_term(
        "My name is Mani.",
        category="personal"
    )

    memories = memory.get_long_term()

    assert len(memories) == 1

    assert (
        memories[0]["content"]
        == "My name is Mani."
    )

    assert (
        memories[0]["category"]
        == "personal"
    )


def test_long_term_search():

    memory = MemoryManager()

    memory.remember_long_term(
        "My name is Mani.",
        category="personal"
    )

    memory.remember_long_term(
        "I am building SARA.",
        category="projects"
    )

    results = memory.search_long_term(
        "SARA"
    )

    assert len(results) == 1

    assert (
        results[0]["content"]
        == "I am building SARA."
    )


def test_long_term_resource_isolation():

    memory = MemoryManager()

    memory.remember_long_term(
        "Python project",
        category="technical"
    )

    results = memory.search_long_term(
        "personal"
    )

    assert results == []


def test_delete_long_term_memory():

    memory = MemoryManager()

    memory.remember_long_term(
        "Memory one"
    )

    memory.remember_long_term(
        "Memory two"
    )

    assert memory.delete_long_term(0)

    memories = memory.get_long_term()

    assert len(memories) == 1

    assert (
        memories[0]["content"]
        == "Memory two"
    )


def test_invalid_delete():

    memory = MemoryManager()

    assert (
        memory.delete_long_term(0)
        is False
    )


def test_memory_category_validation():

    memory = MemoryManager()

    memory.remember_long_term(
        "Something",
        category="invalid"
    )

    memories = memory.get_long_term()

    assert (
        memories[0]["category"]
        == "general"
    )


def test_memory_category_search():

    memory = MemoryManager()

    memory.remember_long_term(
        "Python",
        category="technical"
    )

    memory.remember_long_term(
        "My job",
        category="career"
    )

    results = (
        memory.search_by_category(
            "technical"
        )
    )

    assert len(results) == 1

    assert (
        results[0]["content"]
        == "Python"
    )

def test_long_term_search_requires_relevant_words():

    memory = MemoryManager()

    memory.remember_long_term(
        "I am building SARA.",
        category="projects"
    )

    memory.remember_long_term(
        "My name is Mani.",
        category="personal"
    )

    results = memory.search_long_term(
        "my name"
    )

    assert len(results) == 1

    assert (
        results[0]["content"]
        == "My name is Mani."
    )


def test_long_term_search_ignores_common_words():

    memory = MemoryManager()

    memory.remember_long_term(
        "I am building SARA.",
        category="projects"
    )

    memory.remember_long_term(
        "My name is Mani.",
        category="personal"
    )

    results = memory.search_long_term(
        "my"
    )

    assert results == []


def test_long_term_search_supports_multi_word_query():

    memory = MemoryManager()

    memory.remember_long_term(
        "My favorite programming language is Python.",
        category="preferences"
    )

    memory.remember_long_term(
        "I am building SARA.",
        category="projects"
    )

    results = memory.search_long_term(
        "favorite programming language"
    )

    assert len(results) == 1

    assert (
        results[0]["content"]
        == "My favorite programming language is Python."
    )

# =================================================
# MEMORY STORE
# =================================================


def test_memory_store(tmp_path):

    file_path = (
        tmp_path / "memory.json"
    )

    store = MemoryStore(
        str(file_path)
    )

    store.initialize()

    memories = [
        {
            "content": "My name is Mani.",
            "category": "personal",
            "timestamp": "test"
        }
    ]

    store.save(memories)

    loaded = store.load()

    assert loaded == memories


# =================================================
# CONTEXT MANAGER
# =================================================


def test_context_manager():

    memory = MemoryManager()

    memory.remember_short_term(
        "Hello"
    )

    memory.remember_long_term(
        "My name is Mani.",
        category="personal"
    )

    context = ContextManager(
        memory
    )

    result = context.build_context(
        "Mani"
    )

    assert result["query"] == "Mani"

    assert len(
        result["short_term"]
    ) == 1

    assert len(
        result["long_term"]
    ) == 1


def test_context_format():

    memory = MemoryManager()

    memory.remember_short_term(
        "User: Hello"
    )

    memory.remember_short_term(
        "SARA: Hello Mani."
    )

    memory.remember_long_term(
        "My name is Mani.",
        category="personal"
    )

    context = ContextManager(
        memory
    )

    result = context.format_context(
        "Mani"
    )

    assert (
        "Current request: Mani"
        in result
    )

    assert (
        "User: Hello"
        in result
    )

    assert (
        "SARA: Hello Mani."
        in result
    )

    assert (
        "[personal] My name is Mani."
        in result
    )


def test_context_limits_recent_messages():

    memory = MemoryManager()

    for number in range(10):

        memory.remember_short_term(
            f"Message {number}"
        )

    context = ContextManager(
        memory,
        max_recent_messages=3
    )

    result = context.build_context(
        "test"
    )

    short_term = result[
        "short_term"
    ]

    assert len(short_term) == 3

    assert (
        short_term[0]["content"]
        == "Message 7"
    )

    assert (
        short_term[2]["content"]
        == "Message 9"
    )


def test_context_limits_long_term_memories():

    memory = MemoryManager()

    memory.remember_long_term(
        "Python",
        category="technical"
    )

    memory.remember_long_term(
        "SQL",
        category="technical"
    )

    memory.remember_long_term(
        "Power BI",
        category="technical"
    )

    context = ContextManager(
        memory,
        max_long_term_memories=2
    )

    result = context.build_context(
        "technical"
    )

    assert len(
        result["long_term"]
    ) == 2


def test_context_relevant_memory_limit():

    memory = MemoryManager()

    for number in range(5):

        memory.remember_long_term(
            f"Python memory {number}",
            category="technical"
        )

    context = ContextManager(
        memory,
        max_long_term_memories=2
    )

    results = (
        context.get_relevant_memories(
            "Python"
        )
    )

    assert len(results) == 2


def test_context_format_respects_limits():

    memory = MemoryManager()

    for number in range(5):

        memory.remember_short_term(
            f"Short {number}"
        )

    for number in range(5):

        memory.remember_long_term(
            f"Long {number}",
            category="general"
        )

    context = ContextManager(
        memory,
        max_recent_messages=2,
        max_long_term_memories=2
    )

    result = context.format_context(
        "Long"
    )

    assert "Short 3" in result

    assert "Short 4" in result

    assert "Short 0" not in result

    assert "Long 0" in result

    assert "Long 1" in result


# =================================================
# CONVERSATION MANAGER
# =================================================


def test_conversation_user_message():

    conversation = ConversationManager()

    assert conversation.add_user_message(
        "Hello SARA"
    )

    messages = (
        conversation.get_messages()
    )

    assert len(messages) == 1

    assert (
        messages[0]["role"]
        == "user"
    )

    assert (
        messages[0]["content"]
        == "Hello SARA"
    )


def test_conversation_assistant_message():

    conversation = ConversationManager()

    assert conversation.add_assistant_message(
        "Hello Mani"
    )

    messages = (
        conversation.get_messages()
    )

    assert len(messages) == 1

    assert (
        messages[0]["role"]
        == "assistant"
    )

    assert (
        messages[0]["content"]
        == "Hello Mani"
    )


def test_conversation_preserves_order():

    conversation = ConversationManager()

    conversation.add_user_message(
        "Message one"
    )

    conversation.add_assistant_message(
        "Response one"
    )

    conversation.add_user_message(
        "Message two"
    )

    messages = (
        conversation.get_messages()
    )

    assert len(messages) == 3

    assert (
        messages[0]["content"]
        == "Message one"
    )

    assert (
        messages[1]["content"]
        == "Response one"
    )

    assert (
        messages[2]["content"]
        == "Message two"
    )


def test_conversation_message_limit():

    conversation = ConversationManager(
        max_messages=2
    )

    conversation.add_user_message(
        "One"
    )

    conversation.add_assistant_message(
        "Two"
    )

    conversation.add_user_message(
        "Three"
    )

    messages = (
        conversation.get_messages()
    )

    assert len(messages) == 2

    assert (
        messages[0]["content"]
        == "Two"
    )

    assert (
        messages[1]["content"]
        == "Three"
    )


def test_conversation_recent_messages():

    conversation = ConversationManager(
        max_messages=10
    )

    for number in range(5):

        conversation.add_user_message(
            f"Message {number}"
        )

    recent = (
        conversation.get_recent_messages(
            2
        )
    )

    assert len(recent) == 2

    assert (
        recent[0]["content"]
        == "Message 3"
    )

    assert (
        recent[1]["content"]
        == "Message 4"
    )


def test_conversation_clear():

    conversation = ConversationManager()

    conversation.add_user_message(
        "Hello"
    )

    conversation.add_assistant_message(
        "Hi"
    )

    assert (
        conversation.message_count()
        == 2
    )

    conversation.clear()

    assert (
        conversation.message_count()
        == 0
    )


def test_empty_conversation_message():

    conversation = ConversationManager()

    assert (
        conversation.add_user_message("")
        is False
    )

    assert (
        conversation.add_assistant_message("")
        is False
    )

    assert (
        conversation.message_count()
        == 0
    )


def test_zero_message_limit():

    conversation = ConversationManager(
        max_messages=0
    )

    conversation.add_user_message(
        "Hello"
    )

    assert (
        conversation.message_count()
        == 0
    )


def test_conversation_load_messages():

    conversation = ConversationManager(
        max_messages=10
    )

    messages = [
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hi"
        }
    ]

    assert conversation.load_messages(
        messages
    )

    assert (
        conversation.get_messages()
        == messages
    )


# =================================================
# CONVERSATION CONTEXT
# =================================================


def test_context_includes_conversation():

    memory = MemoryManager()

    conversation = ConversationManager()

    conversation.add_user_message(
        "My name is Mani."
    )

    conversation.add_assistant_message(
        "Nice to meet you, Mani."
    )

    conversation.add_user_message(
        "What is my name?"
    )

    context = ContextManager(
        memory_manager=memory,
        conversation_manager=conversation
    )

    result = context.build_context(
        "What is my name?"
    )

    assert len(
        result["conversation"]
    ) == 3


def test_formatted_context_includes_conversation():

    memory = MemoryManager()

    conversation = ConversationManager()

    conversation.add_user_message(
        "My name is Mani."
    )

    conversation.add_assistant_message(
        "Nice to meet you, Mani."
    )

    context = ContextManager(
        memory_manager=memory,
        conversation_manager=conversation
    )

    result = context.format_context(
        "What is my name?"
    )

    assert (
        "Current conversation:"
        in result
    )

    assert (
        "User: My name is Mani."
        in result
    )

    assert (
        "SARA: Nice to meet you, Mani."
        in result
    )


def test_conversation_context_respects_limit():

    memory = MemoryManager()

    conversation = ConversationManager()

    for number in range(6):

        conversation.add_user_message(
            f"Message {number}"
        )

    context = ContextManager(
        memory_manager=memory,
        conversation_manager=conversation,
        max_recent_messages=3
    )

    result = context.build_context(
        "test"
    )

    messages = result[
        "conversation"
    ]

    assert len(messages) == 3

    assert (
        messages[0]["content"]
        == "Message 3"
    )

    assert (
        messages[2]["content"]
        == "Message 5"
    )


# =================================================
# CONVERSATION STORE
# =================================================


def test_conversation_store(tmp_path):

    file_path = (
        tmp_path / "conversation.json"
    )

    store = ConversationStore(
        str(file_path)
    )

    messages = [
        {
            "role": "user",
            "content": "Hello"
        },
        {
            "role": "assistant",
            "content": "Hi"
        }
    ]

    assert store.save(messages)

    assert (
        store.load()
        == messages
    )


def test_conversation_store_initializes_empty(
    tmp_path
):

    file_path = (
        tmp_path / "conversation.json"
    )

    store = ConversationStore(
        str(file_path)
    )

    store.initialize()

    assert file_path.exists()

    assert store.load() == []


def test_conversation_store_clear(
    tmp_path
):

    file_path = (
        tmp_path / "conversation.json"
    )

    store = ConversationStore(
        str(file_path)
    )

    messages = [
        {
            "role": "user",
            "content": "Hello"
        }
    ]

    store.save(messages)

    assert store.load() == messages

    assert store.clear()

    assert store.load() == []


def test_conversation_store_invalid_json(
    tmp_path
):

    file_path = (
        tmp_path / "conversation.json"
    )

    file_path.write_text(
        "{ invalid json",
        encoding="utf-8"
    )

    store = ConversationStore(
        str(file_path)
    )

    assert store.load() == []


# =================================================
# PROFILE MANAGER
# =================================================


def test_profile_manager():

    profile = ProfileManager()

    assert profile.set(
        "name",
        "Mani"
    )

    assert (
        profile.get("name")
        == "Mani"
    )


def test_profile_manager_load():

    profile = ProfileManager()

    data = {
        "name": "Mani",
        "goal": "Build SARA"
    }

    assert profile.load(data)

    assert (
        profile.get("name")
        == "Mani"
    )

    assert (
        profile.get("goal")
        == "Build SARA"
    )


def test_profile_manager_remove():

    profile = ProfileManager()

    profile.set(
        "name",
        "Mani"
    )

    assert profile.remove(
        "name"
    )

    assert (
        profile.get("name")
        is None
    )


def test_profile_manager_clear():

    profile = ProfileManager()

    profile.set(
        "name",
        "Mani"
    )

    profile.clear()

    assert profile.is_empty()


# =================================================
# PROFILE STORE
# =================================================


def test_profile_store(tmp_path):

    file_path = (
        tmp_path / "profile.json"
    )

    store = ProfileStore(
        str(file_path)
    )

    profile = {
        "name": "Mani",
        "project": "SARA"
    }

    assert store.save(profile)

    assert (
        store.load()
        == profile
    )


def test_profile_store_empty(
    tmp_path
):

    file_path = (
        tmp_path / "profile.json"
    )

    store = ProfileStore(
        str(file_path)
    )

    store.initialize()

    assert file_path.exists()

    assert store.load() == {}


def test_profile_store_clear(
    tmp_path
):

    file_path = (
        tmp_path / "profile.json"
    )

    store = ProfileStore(
        str(file_path)
    )

    store.save({
        "name": "Mani"
    })

    assert store.clear()

    assert store.load() == {}