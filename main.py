from core.sara import Sara
from core.state import SaraState
from core.controller import SaraController
from tools.system_info_tool import SystemInfoTool
from agent.agent import SaraAgent
from agent.runner import AgentRunner

from security.security_manager import (
    SecurityManager
)

from tools.web_search_tool import (
    WebSearchTool
)

from tools.application_launcher import (
    ApplicationLauncher
)

from brain.brain import SaraBrain
from brain.ollama import OllamaProvider

from memory.memory_manager import (
    MemoryManager
)

from memory.memory_store import (
    MemoryStore
)

from memory.conversation_store import (
    ConversationStore
)

from memory.context_manager import (
    ContextManager
)

from memory.conversation_manager import (
    ConversationManager
)

from memory.profile_manager import (
    ProfileManager
)

from memory.profile_store import (
    ProfileStore
)

from tools.tool_registry import (
    ToolRegistry
)

from tools.calculator import (
    CalculatorTool
)

from tools.python_executor import (
    PythonExecutorTool
)

from tools.file_tool import (
    FileTool
)

from tools.file_write_tool import (
    FileWriteTool
)

from tools.datetime_tool import (
    DateTimeTool
)

from voice.voice_manager import (
    VoiceManager
)

from ui.terminal import (
    TerminalUI
)

from config.settings import (
    Settings
)


def create_sara():

    state = SaraState()

    security = SecurityManager(
        state
    )

    sara = Sara(
        security
    )

    provider = OllamaProvider(
        base_url=Settings.AI_BASE_URL,
        model=Settings.AI_MODEL,
        timeout=Settings.AI_TIMEOUT,
        temperature=Settings.AI_TEMPERATURE
    )

    brain = SaraBrain(
        provider=provider
    )

    memory = MemoryManager(
        max_short_term=(
            Settings.MAX_SHORT_TERM_MEMORY
        )
    )

    memory_store = MemoryStore(
        Settings.MEMORY_FILE
    )

    memory_store.initialize()

    memory.long_term_memory = (
        memory_store.load()
    )

    conversation = ConversationManager(
        max_messages=(
            Settings.MAX_CONVERSATION_MESSAGES
        )
    )

    conversation_store = (
        ConversationStore(
            Settings.CONVERSATION_FILE
        )
    )

    conversation_store.initialize()

    conversation.load_messages(
        conversation_store.load()
    )

    profile = ProfileManager()

    profile_store = ProfileStore(
        Settings.PROFILE_FILE
    )

    profile_store.initialize()

    profile.load(
        profile_store.load()
    )

    context = ContextManager(
        memory_manager=memory,
        conversation_manager=conversation,
        profile_manager=profile,
        max_recent_messages=(
            Settings.MAX_CONTEXT_MESSAGES
        ),
        max_long_term_memories=(
            Settings.MAX_CONTEXT_MEMORIES
        )
    )

    tools = ToolRegistry()

    calculator = CalculatorTool()

    tools.register(
        calculator.name,
        calculator
    )

    python_executor = PythonExecutorTool()

    tools.register(
        python_executor.name,
        python_executor
    )

    file_tool = FileTool()

    tools.register(
        file_tool.name,
        file_tool
    )

    file_write_tool = FileWriteTool()

    tools.register(
        file_write_tool.name,
        file_write_tool
    )

    datetime_tool = DateTimeTool()

    tools.register(
        datetime_tool.name,
        datetime_tool
    )

    system_info_tool = SystemInfoTool()

    tools.register(
        system_info_tool.name,
        system_info_tool
    )

    web_search_tool = WebSearchTool()

    tools.register(
        web_search_tool.name,
        web_search_tool
    )

    application_launcher = ApplicationLauncher()

    tools.register(
        application_launcher.name,
        application_launcher
    )

    voice = VoiceManager()

    ui = TerminalUI()

    controller = SaraController(
        sara=sara,
        state=state,
        security=security,
        brain=brain,
        memory=memory,
        context=context,
        conversation=conversation,
        memory_store=memory_store,
        conversation_store=conversation_store,
        profile=profile,
        profile_store=profile_store,
        tools=tools,
        voice=voice,
        ui=ui
    )

    agent = SaraAgent(
        provider=provider,
        tool_registry=tools
    )

    controller.agent = agent

    controller.agent_runner = AgentRunner(
        controller
    )

    return controller


def main():

    controller = create_sara()

    controller.start()


if __name__ == "__main__":

    main()