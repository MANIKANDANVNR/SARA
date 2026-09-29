from agent.security_policy import AgentSecurityPolicy
from core.intent import (
    IntentRouter,
    IntentType
)

from core.memory_detector import (
    MemoryDetector
)

from security.security_gate import (
    SecurityGate
)

from security.permission import (
    PermissionType,
    PermissionLevel
)


class SaraController:

    def __init__(
        self,
        sara,
        state,
        security,
        brain,
        memory,
        context,
        conversation,
        memory_store,
        conversation_store,
        profile,
        profile_store,
        tools,
        voice,
        ui
    ):

        self.sara = sara

        self.state = state

        self.security = security

        self.security_gate = SecurityGate(
            security
        )

        self.brain = brain

        self.memory = memory

        self.context = context

        self.conversation = conversation

        self.memory_store = memory_store

        self.conversation_store = (
            conversation_store
        )

        self.profile = profile

        self.profile_store = profile_store

        self.tools = tools

        self.voice = voice

        self.ui = ui

        self.intent_router = (
            IntentRouter()
        )

        self.memory_detector = (
            MemoryDetector()
        )

    # =================================================
    # START
    # =================================================

    def start(self):

        self.ui.display_banner()

        self.ui.show_message(
            f"Version {self.sara.version}"
        )

        self.ui.show_message(
            "Core system initialized."
        )

        self.ui.show_message(
            "Internet access: OFF"
        )

        self.ui.show_message(
            "File access: OFF"
        )

        self.ui.show_message(
            "System access: OFF"
        )

        self.ui.show_message(
            "Voice system: OFF"
        )

        # -----------------------------------------
        # LOAD PERSISTENT DATA
        # -----------------------------------------

        self.load_persistent_data()

        # -----------------------------------------
        # AI
        # -----------------------------------------

        self.brain.initialize()

        if self.brain.available:

            self.ui.show_message(
                "AI brain: READY"
            )

        else:

            self.ui.show_message(
                "AI brain: OFFLINE"
            )

        self.ui.show_message(
            "Security: ACTIVE"
        )

        self.ui.show_message(
            "Memory: ACTIVE"
        )

        self.ui.show_message(
            "Conversation: ACTIVE"
        )

        self.ui.show_message(
            "Persistent intelligence: ACTIVE"
        )

        self.run()

    # =================================================
    # PERSISTENCE
    # =================================================

    def load_persistent_data(self):

        self.memory.long_term_memory = (
            self.memory_store.load()
        )

        messages = (
            self.conversation_store.load()
        )

        self.conversation.load_messages(
            messages
        )

        profile = (
            self.profile_store.load()
        )

        self.profile.load(
            profile
        )

    def save_conversation(self):

        self.conversation_store.save(
            self.conversation.get_messages()
        )

    def save_memory(self):

        self.memory_store.save(
            self.memory.get_long_term()
        )

    def save_profile(self):

        self.profile_store.save(
            self.profile.get_all()
        )

    # =================================================
    # MAIN LOOP
    # =================================================

    def run(self):

        while self.state.running:

            command = self.ui.get_input()

            if not command:

                continue

            lower = command.lower()

            if lower in {
                "shutdown",
                "exit",
                "quit"
            }:

                self.shutdown()

                continue

            response = self.handle_command(
                command
            )

            if response:

                self.ui.show_message(
                    response
                )

    # =================================================
    # COMMAND HANDLER
    # =================================================

    def handle_command(self, command):

        intent = self.intent_router.route(
            command
        )

        # -----------------------------------------
        # SHUTDOWN
        # -----------------------------------------

        if (
            intent.type
            == IntentType.SHUTDOWN
        ):

            self.shutdown()

            return None

        # -----------------------------------------
        # SECURITY STATUS
        # -----------------------------------------

        if (
            intent.type
            == IntentType.SECURITY_STATUS
        ):

            return self.security_status()

        # -----------------------------------------
        # AUTHENTICATION
        # -----------------------------------------

        if (
            intent.type
            == IntentType.AUTHENTICATE
        ):

            return self.authenticate()

        if (
            intent.type
            == IntentType.AUTHENTICATE_STRONG
        ):

            return self.authenticate_strong()

        if (
            intent.type
            == IntentType.AUTHENTICATE_CRITICAL
        ):

            return self.authenticate_critical()

        # -----------------------------------------
        # LOGOUT
        # -----------------------------------------

        if (
            intent.type
            == IntentType.LOGOUT
        ):

            return self.logout()

        # -----------------------------------------
        # PERMISSIONS
        # -----------------------------------------

        if (
            intent.type
            == IntentType.PERMISSIONS
        ):

            return self.permission_status()

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if (
            intent.type
            == IntentType.EMERGENCY_SHUTDOWN
        ):

            return self.emergency_shutdown()

        # -----------------------------------------
        # CALCULATOR
        # -----------------------------------------

        if (
            intent.type
            == IntentType.CALCULATOR
        ):

            return self.handle_calculator(
                intent.value
            )

        # -----------------------------------------
        # PYTHON
        # -----------------------------------------

        if (
            intent.type
            == IntentType.PYTHON
        ):

            return self.handle_python(
                intent.value
            )

        # -----------------------------------------
        # FILE WRITE
        # -----------------------------------------

        if (
            intent.type
            == IntentType.FILE_WRITE
        ):

            return self.handle_file_write(
                intent.value
            )

        # -----------------------------------------
        # DATE & TIME
        # -----------------------------------------

        if (
            intent.type
            == IntentType.DATETIME
        ):

            return self.handle_datetime()

        # -----------------------------------------
        # SYSTEM INFO
        # -----------------------------------------

        if (
            intent.type
            == IntentType.SYSTEM_INFO
        ):

            return self.handle_system_info()

        # -----------------------------------------
        # WEB SEARCH
        # -----------------------------------------

        if (
            intent.type
            == IntentType.WEB_SEARCH
        ):

            return self.handle_web_search(
                intent.value
            )

        # -----------------------------------------
        # APPLICATION LAUNCHER
        # -----------------------------------------

        if (
            intent.type
            == IntentType.APPLICATION_LAUNCH
        ):

            return self.handle_application_launch(
                intent.value
            )

        # -----------------------------------------
        # AI STATUS
        # -----------------------------------------

        if (
            intent.type
            == IntentType.AI_STATUS
        ):

            return self.ai_status()

        # -----------------------------------------
        # AGENT
        # -----------------------------------------

        if (
            intent.type
            == IntentType.AGENT
        ):

            return self.handle_agent(
                intent.value
            )

        # -----------------------------------------
        # AI
        # -----------------------------------------

        if (
            intent.type
            == IntentType.AI
        ):

            return self.ask_ai(
                intent.value
            )

        # -----------------------------------------
        # MEMORY
        # -----------------------------------------

        if (
            intent.type
            == IntentType.MEMORY_STATUS
        ):

            return self.memory_status()

        if (
            intent.type
            == IntentType.MEMORY_SHORT
        ):

            return self.format_short_memory()

        if (
            intent.type
            == IntentType.MEMORY_LONG
        ):

            return self.format_long_memory()

        if (
            intent.type
            == IntentType.MEMORY_CLEAR_SHORT
        ):

            self.memory.clear_short_term()

            return (
                "Short-term memory cleared."
            )

        if (
            intent.type
            == IntentType.MEMORY_CLEAR_LONG
        ):

            if not self.state.authenticated:

                return (
                    "Permission denied. "
                    "Authentication required."
                )

            self.memory.clear_long_term()

            self.save_memory()

            self.security.audit.record(
                event="MEMORY_CLEARED",
                action="clear_long_term",
                resource="long_term_memory",
                result="success"
            )

            return (
                "Long-term memory cleared."
            )

        if (
            intent.type
            == IntentType.MEMORY_REMEMBER
        ):

            return self.remember_long_term(
                intent.value
            )

        if (
            intent.type
            == IntentType.MEMORY_RECALL
        ):

            return self.recall(
                intent.value
            )

        # -----------------------------------------
        # MEMORY FORGET
        # -----------------------------------------

        if (
            intent.type
            == IntentType.MEMORY_FORGET
        ):

            return self.forget(
                intent.value
            )

        if (
            intent.type
            == IntentType.MEMORY_CATEGORY
        ):

            return self.memory_category(
                intent.value
            )

        # -----------------------------------------
        # CONVERSATION
        # -----------------------------------------

        if (
            intent.type
            == IntentType.CONVERSATION_STATUS
        ):

            return self.conversation_status()

        if (
            intent.type
            == IntentType.CONVERSATION_CLEAR
        ):

            if not self.state.authenticated:

                return (
                    "Permission denied. "
                    "Authentication required."
                )

            self.conversation.clear()

            self.save_conversation()

            self.security.audit.record(
                event="CONVERSATION_CLEARED",
                action="clear",
                resource="conversation_history",
                result="success"
            )

            return (
                "Conversation history cleared."
            )

        # -----------------------------------------
        # PROFILE
        # -----------------------------------------

        if (
            intent.type
            == IntentType.PROFILE_STATUS
        ):

            return self.profile_status()

        if (
            intent.type
            == IntentType.PROFILE_SET
        ):

            if not self.state.authenticated:

                return (
                    "Permission denied. "
                    "Authentication required."
                )

            profile_data = intent.value

            if not isinstance(
                profile_data,
                dict
            ):

                return (
                    "Invalid profile data."
                )

            key = profile_data.get(
                "key"
            )

            value = profile_data.get(
                "value"
            )

            if not key or not value:

                return (
                    "Invalid profile data."
                )

            if not self.profile.set(
                key,
                value
            ):

                return (
                    "Failed to update user profile."
                )

            self.save_profile()

            self.security.audit.record(
                event="PROFILE_UPDATED",
                action="set",
                resource="user_profile",
                result="success"
            )

            return (
                f"Profile updated: "
                f"{str(key).strip().lower()} = "
                f"{value}"
            )

        if (
            intent.type
            == IntentType.PROFILE_CLEAR
        ):

            if not self.state.authenticated:

                return (
                    "Permission denied. "
                    "Authentication required."
                )

            self.profile.clear()

            self.save_profile()

            self.security.audit.record(
                event="PROFILE_CLEARED",
                action="clear",
                resource="user_profile",
                result="success"
            )

            return (
                "User profile cleared."
            )

        return None

    # =================================================
    # APPLICATION LAUNCHER
    # =================================================

    def handle_application_launch(
        self,
        application
    ):

        if not application:

            return (
                "Application name cannot be empty."
            )

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="APPLICATION_LAUNCH_REQUEST",
                action="launch",
                resource=application,
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # AUTHENTICATION
        # -----------------------------------------

        if not self.state.authenticated:

            self.security.audit.record(
                event="APPLICATION_LAUNCH_REQUEST",
                action="launch",
                resource=application,
                result="NOT_AUTHENTICATED"
            )

            return (
                "Permission denied. "
                "Authentication required "
                "to launch applications."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "application_launcher"
        ):

            self.security.audit.record(
                event="APPLICATION_LAUNCH_REQUEST",
                action="launch",
                resource=application,
                result="TOOL_NOT_FOUND"
            )

            return (
                "Application Launcher tool is unavailable."
            )

        # -----------------------------------------
        # SYSTEM PERMISSION
        # -----------------------------------------

        if not self.security.has_permission(
            PermissionType.SYSTEM
        ):

            granted = (
                self.request_tool_access(
                    tool_name="application_launcher",
                    permission_type=(
                        PermissionType.SYSTEM
                    ),
                    level=PermissionLevel.MEDIUM
                )
            )

            if not granted:

                self.security.audit.record(
                    event="APPLICATION_LAUNCH_REQUEST",
                    action="launch",
                    resource=application,
                    result="PERMISSION_DENIED"
                )

                return (
                    "System access permission denied."
                )

        # -----------------------------------------
        # EXECUTE APPLICATION LAUNCH
        # -----------------------------------------

        result = self.execute_application_launch(
            application
        )

        if not result["success"]:

            self.security.audit.record(
                event="APPLICATION_LAUNCH_REQUEST",
                action="launch",
                resource=application,
                result="FAILED"
            )

            return (
                f"Application launch failed: "
                f"{result['error']}"
            )

        self.security.audit.record(
            event="APPLICATION_LAUNCH_REQUEST",
            action="launch",
            resource=application,
            result="SUCCESS"
        )

        launched_application = result[
            "result"
        ]

        if not isinstance(
            launched_application,
            dict
        ):

            return (
                "Invalid Application Launcher "
                "tool response."
            )

        launched = launched_application.get(
            "launched"
        )

        if not launched:

            return (
                "Application Launcher tool "
                "reported an invalid result."
            )

        application_name = (
            launched_application.get(
                "application"
            )
            or application
        )

        return (
            f"Application launched successfully: "
            f"{application_name}"
        )

    # =================================================
    # CALCULATOR
    # =================================================

    def handle_calculator(
        self,
        expression
    ):

        if not expression:

            return (
                "Calculator expression "
                "cannot be empty."
            )

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="CALCULATOR_REQUEST",
                action="calculate",
                resource="calculator",
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # AUTHENTICATION
        # -----------------------------------------

        if not self.state.authenticated:

            self.security.audit.record(
                event="CALCULATOR_REQUEST",
                action="calculate",
                resource="calculator",
                result="NOT_AUTHENTICATED"
            )

            return (
                "Permission denied. "
                "Authentication required "
                "to use the calculator."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "calculator"
        ):

            self.security.audit.record(
                event="CALCULATOR_REQUEST",
                action="calculate",
                resource="calculator",
                result="TOOL_NOT_FOUND"
            )

            return (
                "Calculator tool is unavailable."
            )

        # -----------------------------------------
        # CALCULATOR PERMISSION
        # -----------------------------------------

        if not self.security.has_permission(
            PermissionType.CALCULATOR
        ):

            granted = (
                self.request_tool_access(
                    tool_name="calculator",
                    permission_type=(
                        PermissionType.CALCULATOR
                    ),
                    level=PermissionLevel.LOW
                )
            )

            if not granted:

                self.security.audit.record(
                    event="CALCULATOR_REQUEST",
                    action="calculate",
                    resource="calculator",
                    result="PERMISSION_DENIED"
                )

                return (
                    "Calculator permission denied."
                )

        # -----------------------------------------
        # EXECUTE CALCULATION
        # -----------------------------------------

        result = self.execute_calculator(
            expression
        )

        if not result["success"]:

            return (
                f"Calculation failed: "
                f"{result['error']}"
            )

        self.security.audit.record(
            event="CALCULATOR_REQUEST",
            action="calculate",
            resource="calculator",
            result="SUCCESS"
        )

        return (
            f"Result: {result['result']}"
        )

    # =================================================
    # PYTHON
    # =================================================

    def handle_python(
        self,
        code
    ):

        if not code:

            return (
                "Python code cannot be empty."
            )

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="PYTHON_REQUEST",
                action="execute",
                resource="python",
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # AUTHENTICATION
        # -----------------------------------------

        if not self.state.authenticated:

            self.security.audit.record(
                event="PYTHON_REQUEST",
                action="execute",
                resource="python",
                result="NOT_AUTHENTICATED"
            )

            return (
                "Permission denied. "
                "Authentication required "
                "to use Python execution."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "python"
        ):

            self.security.audit.record(
                event="PYTHON_REQUEST",
                action="execute",
                resource="python",
                result="TOOL_NOT_FOUND"
            )

            return (
                "Python execution tool is unavailable."
            )

        # -----------------------------------------
        # PYTHON PERMISSION
        # -----------------------------------------

        if not self.security.has_permission(
            PermissionType.PYTHON
        ):

            granted = (
                self.request_tool_access(
                    tool_name="python",
                    permission_type=(
                        PermissionType.PYTHON
                    ),
                    level=PermissionLevel.LOW
                )
            )

            if not granted:

                self.security.audit.record(
                    event="PYTHON_REQUEST",
                    action="execute",
                    resource="python",
                    result="PERMISSION_DENIED"
                )

                return (
                    "Python execution permission denied."
                )

        # -----------------------------------------
        # EXECUTE PYTHON
        # -----------------------------------------

        result = self.execute_python(
            code
        )

        if not result["success"]:

            self.security.audit.record(
                event="PYTHON_REQUEST",
                action="execute",
                resource="python",
                result="FAILED"
            )

            return (
                f"Python execution failed: "
                f"{result['error']}"
            )

        self.security.audit.record(
            event="PYTHON_REQUEST",
            action="execute",
            resource="python",
            result="SUCCESS"
        )

        if result["result"] is None:

            return (
                "Python execution completed successfully."
            )

        return (
            f"Python result:\n"
            f"{result['result']}"
        )

    # =================================================
    # FILE WRITE
    # =================================================

    def handle_file_write(
        self,
        file_data
    ):

        if not isinstance(
            file_data,
            dict
        ):

            return (
                "Invalid file write data."
            )

        path = file_data.get(
            "path"
        )

        content = file_data.get(
            "content"
        )

        if not path:

            return (
                "File path cannot be empty."
            )

        if content is None:

            return (
                "File content cannot be empty."
            )

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="FILE_WRITE_REQUEST",
                action="write",
                resource=path,
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # AUTHENTICATION
        # -----------------------------------------

        if not self.state.authenticated:

            self.security.audit.record(
                event="FILE_WRITE_REQUEST",
                action="write",
                resource=path,
                result="NOT_AUTHENTICATED"
            )

            return (
                "Permission denied. "
                "Authentication required "
                "to write files."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "file_write"
        ):

            self.security.audit.record(
                event="FILE_WRITE_REQUEST",
                action="write",
                resource=path,
                result="TOOL_NOT_FOUND"
            )

            return (
                "File write tool is unavailable."
            )

        # -----------------------------------------
        # FILE WRITE PERMISSION
        # -----------------------------------------

        if not self.security.has_permission(
            PermissionType.WRITE_FILE,
            resource=path
        ):

            granted = (
                self.request_tool_access(
                    tool_name="file_write",
                    permission_type=(
                        PermissionType.WRITE_FILE
                    ),
                    level=PermissionLevel.LOW,
                    resource=path
                )
            )

            if not granted:

                self.security.audit.record(
                    event="FILE_WRITE_REQUEST",
                    action="write",
                    resource=path,
                    result="PERMISSION_DENIED"
                )

                return (
                    "File write permission denied."
                )

        # -----------------------------------------
        # EXECUTE FILE WRITE
        # -----------------------------------------

        result = self.execute_file_write(
            path=path,
            content=content
        )

        if not result["success"]:

            self.security.audit.record(
                event="FILE_WRITE_REQUEST",
                action="write",
                resource=path,
                result="FAILED"
            )

            return (
                f"File write failed: "
                f"{result['error']}"
            )

        self.security.audit.record(
            event="FILE_WRITE_REQUEST",
            action="write",
            resource=path,
            result="SUCCESS"
        )

        return (
            f"File written successfully: "
            f"{result['result']}"
        )

    # =================================================
    # DATE & TIME
    # =================================================

    def handle_datetime(self):

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="DATETIME_REQUEST",
                action="datetime",
                resource="datetime",
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "datetime"
        ):

            self.security.audit.record(
                event="DATETIME_REQUEST",
                action="datetime",
                resource="datetime",
                result="TOOL_NOT_FOUND"
            )

            return (
                "Date & Time tool is unavailable."
            )

        # -----------------------------------------
        # EXECUTE DATE & TIME TOOL
        # -----------------------------------------

        tool = self.get_tool(
            "datetime"
        )

        try:

            result = tool.execute()

        except Exception as error:

            self.security.audit.record(
                event="DATETIME_REQUEST",
                action="datetime",
                resource="datetime",
                result="FAILED"
            )

            return (
                f"Date & Time request failed: "
                f"{error}"
            )

        self.security.audit.record(
            event="DATETIME_REQUEST",
            action="datetime",
            resource="datetime",
            result="SUCCESS"
        )

        if not isinstance(
            result,
            dict
        ):

            return (
                "Invalid Date & Time tool response."
            )

        date = result.get(
            "date"
        )

        time = result.get(
            "time"
        )

        day = result.get(
            "day"
        )

        if not date or not time or not day:

            return (
                "Invalid Date & Time tool response."
            )

        return (
            "DATE & TIME\n"
            "-----------\n"
            f"Date: {date}\n"
            f"Time: {time}\n"
            f"Day: {day}"
        )

    # =================================================
    # SYSTEM INFO
    # =================================================

    def handle_system_info(self):

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="SYSTEM_INFO_REQUEST",
                action="system_info",
                resource="system_info",
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "system_info"
        ):

            self.security.audit.record(
                event="SYSTEM_INFO_REQUEST",
                action="system_info",
                resource="system_info",
                result="TOOL_NOT_FOUND"
            )

            return (
                "System Info tool is unavailable."
            )

        # -----------------------------------------
        # EXECUTE SYSTEM INFO TOOL
        # -----------------------------------------

        tool = self.get_tool(
            "system_info"
        )

        try:

            result = tool.execute()

        except Exception as error:

            self.security.audit.record(
                event="SYSTEM_INFO_REQUEST",
                action="system_info",
                resource="system_info",
                result="FAILED"
            )

            return (
                f"System Info request failed: "
                f"{error}"
            )

        self.security.audit.record(
            event="SYSTEM_INFO_REQUEST",
            action="system_info",
            resource="system_info",
            result="SUCCESS"
        )

        # -----------------------------------------
        # VALIDATE RESULT
        # -----------------------------------------

        if not isinstance(
            result,
            dict
        ):

            return (
                "Invalid System Info tool response."
            )

        operating_system = result.get(
            "operating_system"
        )

        os_release = result.get(
            "os_release"
        )

        os_version = result.get(
            "os_version"
        )

        machine = result.get(
            "machine"
        )

        processor = result.get(
            "processor"
        )

        python_version = result.get(
            "python_version"
        )

        architecture = result.get(
            "architecture"
        )

        if not operating_system:

            return (
                "Invalid System Info tool response."
            )

        if not os_release:

            return (
                "Invalid System Info tool response."
            )

        if not os_version:

            return (
                "Invalid System Info tool response."
            )

        if not machine:

            return (
                "Invalid System Info tool response."
            )

        if not python_version:

            return (
                "Invalid System Info tool response."
            )

        if not architecture:

            return (
                "Invalid System Info tool response."
            )

        if not processor:

            processor = "Unknown"

        return (
            "SYSTEM INFORMATION\n"
            "------------------\n"
            f"Operating System: "
            f"{operating_system}\n"
            f"OS Release: "
            f"{os_release}\n"
            f"OS Version: "
            f"{os_version}\n"
            f"Machine: "
            f"{machine}\n"
            f"Processor: "
            f"{processor}\n"
            f"Architecture: "
            f"{architecture}\n"
            f"Python Version: "
            f"{python_version}"
        )

    # =================================================
    # WEB SEARCH
    # =================================================

    def handle_web_search(
        self,
        query
    ):

        if not query:

            return (
                "Search query cannot be empty."
            )

        # -----------------------------------------
        # EMERGENCY SHUTDOWN
        # -----------------------------------------

        if self.state.emergency_shutdown:

            self.security.audit.record(
                event="WEB_SEARCH_REQUEST",
                action="search",
                resource="web",
                result="EMERGENCY_SHUTDOWN"
            )

            return (
                "Permission denied. "
                "Emergency shutdown is active."
            )

        # -----------------------------------------
        # AUTHENTICATION
        # -----------------------------------------

        if not self.state.authenticated:

            self.security.audit.record(
                event="WEB_SEARCH_REQUEST",
                action="search",
                resource="web",
                result="NOT_AUTHENTICATED"
            )

            return (
                "Permission denied. "
                "Authentication required "
                "to search the web."
            )

        # -----------------------------------------
        # TOOL EXISTENCE
        # -----------------------------------------

        if not self.tool_exists(
            "web_search"
        ):

            self.security.audit.record(
                event="WEB_SEARCH_REQUEST",
                action="search",
                resource="web",
                result="TOOL_NOT_FOUND"
            )

            return (
                "Web Search tool is unavailable."
            )

        # -----------------------------------------
        # INTERNET PERMISSION
        # -----------------------------------------

        if not self.security.has_permission(
            PermissionType.INTERNET
        ):

            granted = (
                self.request_tool_access(
                    tool_name="web_search",
                    permission_type=(
                        PermissionType.INTERNET
                    ),
                    level=PermissionLevel.MEDIUM
                )
            )

            if not granted:

                self.security.audit.record(
                    event="WEB_SEARCH_REQUEST",
                    action="search",
                    resource="web",
                    result="PERMISSION_DENIED"
                )

                return (
                    "Internet access permission denied."
                )

        # -----------------------------------------
        # EXECUTE WEB SEARCH
        # -----------------------------------------

        result = self.execute_web_search(
            query
        )

        if not result["success"]:

            self.security.audit.record(
                event="WEB_SEARCH_REQUEST",
                action="search",
                resource="web",
                result="FAILED"
            )

            return (
                f"Web search failed: "
                f"{result['error']}"
            )

        self.security.audit.record(
            event="WEB_SEARCH_REQUEST",
            action="search",
            resource="web",
            result="SUCCESS"
        )

        search_results = result["result"]

        # -----------------------------------------
        # VALIDATE RESULTS
        # -----------------------------------------

        if not isinstance(
            search_results,
            list
        ):

            return (
                "Invalid Web Search tool response."
            )

        if not search_results:

            return (
                "No search results found."
            )

        # -----------------------------------------
        # FORMAT RESULTS
        # -----------------------------------------

        lines = [
            "WEB SEARCH RESULTS",
            "------------------"
        ]

        for index, item in enumerate(
            search_results,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):

                continue

            title = item.get(
                "title"
            )

            url = item.get(
                "url"
            )

            if not title or not url:

                continue

            lines.append(
                f"{index}. {title}"
            )

            lines.append(
                f"   {url}"
            )

        if len(lines) == 2:

            return (
                "Invalid Web Search tool response."
            )

        return "\n".join(
            lines
        )

    # =================================================
    # TOOL REGISTRY
    # =================================================

    def register_tool(self, name, tool):

        if self.tools is None:

            return False

        return self.tools.register(
            name,
            tool
        )

    def get_tool(self, name):

        if self.tools is None:

            return None

        return self.tools.get(
            name
        )

    def tool_exists(self, name):

        if self.tools is None:

            return False

        return self.tools.exists(
            name
        )

    def list_tools(self):

        if self.tools is None:

            return []

        return self.tools.list_tools()

    def tool_count(self):

        if self.tools is None:

            return 0

        if hasattr(
            self.tools,
            "count"
        ):

            return self.tools.count()

        return len(
            self.tools.list_tools()
        )

    def tool_definitions(self):

        if self.tools is None:

            return []

        if hasattr(
            self.tools,
            "get_definitions"
        ):

            return self.tools.get_definitions()

        return []

    # =================================================
    # AGENT
    # =================================================

    def handle_agent(
        self,
        request
    ):

        if not request:
            return (
                "Agent request cannot be empty."
            )

        if not self.state.authenticated:
            return (
                "Permission denied. "
                "Authentication required "
                "to use agent mode."
            )

        if not hasattr(
            self,
            "agent"
        ) or self.agent is None:

            return (
                "Agent is not available."
            )

        if not hasattr(
            self,
            "agent_runner"
        ) or self.agent_runner is None:

            return (
                "Agent runner is not available."
            )

        try:

            task = self.agent.create_plan(
                request=request,
                context=self.context
            )

        except Exception as error:

            self.security.audit.record(
                event="AGENT_PLAN_FAILED",
                action="create_plan",
                resource=request,
                result=str(error)
            )

            return (
                "Agent planning failed: "
                f"{error}"
            )

        policy = AgentSecurityPolicy()

        for step in task.steps:

            tool_name = (
                str(step.tool_name)
                .strip()
                .lower()
            )

            tool_policy = policy.get_policy(
                tool_name
            )

            if tool_policy is None:

                task.status = "failed"

                task.error = (
                    "Security policy unavailable "
                    f"for tool '{tool_name}'."
                )

                self.security.audit.record(
                    event="AGENT_SECURITY_DENIED",
                    action=tool_name,
                    resource=None,
                    result="POLICY_UNAVAILABLE"
                )

                return task.error

            permission_type = (
                tool_policy[
                    "permission_type"
                ]
            )

            level = (
                tool_policy[
                    "level"
                ]
            )

            resource = (
                policy.get_resource(
                    tool_name,
                    step.arguments
                )
            )

            if not self.security.has_permission(
                permission_type,
                resource=resource
            ):

                granted = (
                    self.request_tool_access(
                        tool_name=tool_name,
                        permission_type=permission_type,
                        level=level,
                        resource=resource
                    )
                )

                if not granted:

                    task.status = "failed"

                    task.error = (
                        "Agent permission denied "
                        f"for tool '{tool_name}'."
                    )

                    return task.error

        task = self.agent_runner.run(
            task=task,
            permission_type=None,
            level=None
        )

        if task.status == "completed":

            if task.result is not None:
                return str(task.result)

            return (
                task.report
                if task.report
                else "Agent task completed successfully."
            )

        return (
            task.error
            if task.error
            else "Agent task failed."
        )

    # =================================================
    # TOOL SECURITY
    # =================================================

    def request_tool_access(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        duration=None
    ):

        if not self.tool_exists(
            tool_name
        ):

            return False

        return self.security_gate.request_tool_access(
            tool_name=tool_name,
            permission_type=permission_type,
            level=level,
            resource=resource,
            duration=duration
        )

    def authorize_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None
    ):

        if not self.tool_exists(
            tool_name
        ):

            return False

        return self.security_gate.authorize_tool(
            tool_name=tool_name,
            permission_type=permission_type,
            level=level,
            resource=resource
        )

    def execute_tool(
        self,
        tool_name,
        permission_type,
        level,
        *args,
        resource=None,
        **kwargs
    ):

        if not self.tool_exists(
            tool_name
        ):

            self.security.audit.record(
                event="TOOL_EXECUTION",
                action=str(tool_name),
                resource=resource,
                result="TOOL_NOT_FOUND"
            )

            return {
                "success": False,
                "result": None,
                "error": "Tool not found."
            }

        authorized = (
            self.security_gate.authorize_tool(
                tool_name=tool_name,
                permission_type=permission_type,
                level=level,
                resource=resource
            )
        )

        if not authorized:

            self.security.audit.record(
                event="TOOL_EXECUTION",
                action=str(tool_name),
                resource=resource,
                result="PERMISSION_DENIED"
            )

            return {
                "success": False,
                "result": None,
                "error": (
                    "Tool execution permission denied."
                )
            }

        tool = self.get_tool(
            tool_name
        )

        try:

            result = tool.execute(
                *args,
                **kwargs
            )

            self.security.audit.record(
                event="TOOL_EXECUTION",
                action=str(tool_name),
                resource=resource,
                result="SUCCESS"
            )

            return {
                "success": True,
                "result": result,
                "error": None
            }

        except Exception as error:

            self.security.audit.record(
                event="TOOL_EXECUTION",
                action=str(tool_name),
                resource=resource,
                result="FAILED"
            )

            return {
                "success": False,
                "result": None,
                "error": str(error)
            }

    def execute_calculator(
        self,
        expression
    ):

        return self.execute_tool(
            tool_name="calculator",
            permission_type=PermissionType.CALCULATOR,
            level=PermissionLevel.LOW,
            expression=expression
        )

    def execute_file(
        self,
        path,
        encoding=None
    ):

        return self.execute_tool(
            tool_name="file",
            permission_type=PermissionType.READ_FILE,
            level=PermissionLevel.LOW,
            resource=path,
            path=path,
            encoding=encoding
        )

    def execute_file_write(
        self,
        path,
        content,
        encoding=None
    ):

        return self.execute_tool(
            tool_name="file_write",
            permission_type=PermissionType.WRITE_FILE,
            level=PermissionLevel.LOW,
            resource=path,
            path=path,
            content=content,
            encoding=encoding
        )

    def execute_python(
        self,
        code
    ):

        return self.execute_tool(
            tool_name="python",
            permission_type=PermissionType.PYTHON,
            level=PermissionLevel.LOW,
            code=code
        )

    def execute_web_search(
        self,
        query,
        max_results=None
    ):

        return self.execute_tool(
            tool_name="web_search",
            permission_type=PermissionType.INTERNET,
            level=PermissionLevel.MEDIUM,
            query=query,
            max_results=max_results
        )

    def execute_application_launch(
        self,
        application
    ):

        return self.execute_tool(
            tool_name="application_launcher",
            permission_type=PermissionType.SYSTEM,
            level=PermissionLevel.MEDIUM,
            application=application
        )

    # =================================================
    # SECURITY
    # =================================================

    def security_status(self):

        status = (
            self.security
            .get_security_status()
        )

        permissions = status[
            "active_permissions"
        ]

        if permissions:

            permission_text = ", ".join(
                permissions
            )

        else:

            permission_text = "None"

        return (
            "SECURITY STATUS\n"
            "---------------\n"
            f"Authenticated: "
            f"{status['authenticated']}\n"
            f"Authentication Level: "
            f"{status['authentication_level']}\n"
            f"Active Permissions: "
            f"{permission_text}\n"
            f"Emergency Shutdown: "
            f"{status['emergency_shutdown']}"
        )

    def authenticate(self):

        if self.security.authenticate():

            self.security.audit.record(
                event="AUTHENTICATION",
                action="authenticate",
                resource="security",
                result="success"
            )

            return (
                "Basic authentication successful."
            )

        self.security.audit.record(
            event="AUTHENTICATION",
            action="authenticate",
            resource="security",
            result="failed"
        )

        return "Authentication failed."

    def authenticate_strong(self):

        if self.security.authenticate_strong():

            self.security.audit.record(
                event="AUTHENTICATION",
                action="authenticate_strong",
                resource="security",
                result="success"
            )

            return (
                "Strong authentication successful."
            )

        return (
            "Strong authentication failed. "
            "Basic authentication is required first."
        )

    def authenticate_critical(self):

        if self.security.authenticate_critical():

            self.security.audit.record(
                event="AUTHENTICATION",
                action="authenticate_critical",
                resource="security",
                result="success"
            )

            return (
                "Critical authentication successful."
            )

        return (
            "Critical authentication failed. "
            "Basic authentication is required first."
        )

    def logout(self):

        self.security.logout()

        self.security.audit.record(
            event="LOGOUT",
            action="logout",
            resource="security",
            result="success"
        )

        return "You have been logged out."

    def permission_status(self):

        return self.security_status()

    def emergency_shutdown(self):

        self.security.emergency_shutdown()

        self.security.audit.record(
            event="EMERGENCY_SHUTDOWN",
            action="emergency_shutdown",
            resource="security",
            result="success"
        )

        return "Emergency shutdown activated."

    # =================================================
    # AI
    # =================================================

    def ask_ai(self, prompt):

        if not prompt:

            return (
                "Please provide something "
                "for me to think about."
            )

        if not self.brain.available:

            return (
                "My AI brain is currently "
                "offline."
            )

        self.memory.remember_short_term(
            f"User: {prompt}"
        )

        self.conversation.add_user_message(
            prompt
        )

        context = (
            self.context
            .format_context(prompt)
        )

        response = self.brain.think(
            prompt=prompt,
            context=context
        )

        self.save_automatic_memory(
            prompt
        )

        self.memory.remember_short_term(
            f"SARA: {response}"
        )

        self.conversation.add_assistant_message(
            response
        )

        self.save_conversation()

        self.security.audit.record(
            event="AI_REQUEST",
            action="generate",
            resource="ai_brain",
            result="success"
        )

        return response

    # =================================================
    # AUTOMATIC MEMORY
    # =================================================

    def save_automatic_memory(self, prompt):

        if not self.state.authenticated:

            return False

        if not prompt:

            return False

        result = (
            self.memory_detector.detect(
                prompt
            )
        )

        if result is None:

            return False

        content = result["content"]

        category = result["category"]

        normalized_content = (
            content.strip().lower()
        )

        for memory in (
            self.memory.get_long_term()
        ):

            existing_content = (
                memory.get(
                    "content",
                    ""
                )
                .strip()
                .lower()
            )

            if (
                existing_content
                == normalized_content
            ):

                return False

        saved = (
            self.memory.remember_long_term(
                content,
                category=category
            )
        )

        if not saved:

            return False

        self.save_memory()

        self.security.audit.record(
            event="MEMORY_CREATED",
            action="automatic_remember",
            resource="long_term_memory",
            result="success"
        )

        return True

    # =================================================
    # AI STATUS
    # =================================================

    def ai_status(self):

        status = self.brain.status()

        availability = (
            "READY"
            if status["available"]
            else "OFFLINE"
        )

        provider = (
            status["provider"]
            or "None"
        )

        model = (
            status["model"]
            or "None"
        )

        return (
            "AI STATUS\n"
            "---------\n"
            f"Status: {availability}\n"
            f"Provider: {provider}\n"
            f"Model: {model}\n"
            f"Tools enabled: "
            f"{self.brain_tools_enabled()}\n"
            f"File access: "
            f"{self.ai_file_access_enabled()}\n"
            f"Internet access: "
            f"{self.ai_internet_access_enabled()}\n"
            f"System access: "
            f"{self.ai_system_access_enabled()}"
        )

    def brain_tools_enabled(self):

        return self.tool_count() > 0

    def ai_file_access_enabled(self):

        return False

    def ai_internet_access_enabled(self):

        return False

    def ai_system_access_enabled(self):

        return False

    # =================================================
    # LONG-TERM MEMORY
    # =================================================

    def remember_long_term(self, content):

        if not self.state.authenticated:
            return (
                "Permission denied. "
                "Authentication required "
                "to store long-term memory."
            )

        if not content:
            return (
                "Memory content cannot be empty."
            )

        normalized_content = (
            str(content)
            .strip()
            .lower()
        )

        if not normalized_content:
            return (
                "Memory content cannot be empty."
            )

        for memory in (
                self.memory.get_long_term()
        ):

            existing_content = (
                str(
                    memory.get(
                        "content",
                        ""
                    )
                )
                .strip()
                .lower()
            )

            if (
                    existing_content
                    == normalized_content
            ):
                return (
                    "That memory already exists."
                )

        category = (
            self.detect_memory_category(
                content
            )
        )

        saved = (
            self.memory.remember_long_term(
                content,
                category=category
            )
        )

        if not saved:
            return (
                "Unable to store that memory."
            )

        self.save_memory()

        self.security.audit.record(
            event="MEMORY_CREATED",
            action="remember",
            resource="long_term_memory",
            result="success"
        )

        return (
            f"I will remember that "
            f"under {category} memory."
        )

    # =================================================
    # MEMORY CATEGORY DETECTION
    # =================================================

    def detect_memory_category(
        self,
        content
    ):

        text = content.lower()

        personal_words = {
            "my name",
            "i am",
            "i'm",
            "my age",
            "my birthday",
            "my family"
        }

        preference_words = {
            "i like",
            "i love",
            "i prefer",
            "i don't like",
            "my favorite"
        }

        career_words = {
            "job",
            "career",
            "resume",
            "salary",
            "company",
            "developer",
            "analyst",
            "interview"
        }

        project_words = {
            "project",
            "sara",
            "software",
            "application",
            "website",
            "app",
            "game"
        }

        technical_words = {
            "python",
            "sql",
            "mysql",
            "power bi",
            "programming",
            "coding",
            "computer",
            "linux",
            "windows",
            "api"
        }

        if any(
            word in text
            for word in personal_words
        ):

            return "personal"

        if any(
            word in text
            for word in preference_words
        ):

            return "preferences"

        if any(
            word in text
            for word in career_words
        ):

            return "career"

        if any(
            word in text
            for word in project_words
        ):

            return "projects"

        if any(
            word in text
            for word in technical_words
        ):

            return "technical"

        return "general"

    # =================================================
    # MEMORY RECALL
    # =================================================

    def recall(self, query):

        results = (
            self.memory
            .search_long_term(query)
        )

        if not results:

            return (
                "I couldn't find anything "
                "matching that memory."
            )

        lines = [
            "MEMORY SEARCH",
            "-------------"
        ]

        for memory in results:

            lines.append(
                f"[{memory['category']}] "
                f"{memory['content']}"
            )

        return "\n".join(lines)

    # =================================================
    # MEMORY FORGET
    # =================================================

    def forget(self, query):

        if not self.state.authenticated:

            return (
                "Permission denied. "
                "Authentication required "
                "to forget long-term memory."
            )

        if not query:

            return (
                "Memory query cannot be empty."
            )

        query = str(query).strip()

        if not query:

            return (
                "Memory query cannot be empty."
            )

        results = (
            self.memory
            .search_long_term(query)
        )

        if not results:

            return (
                "I couldn't find any memory "
                "matching that request."
            )

        if len(results) > 1:

            lines = [
                "Multiple memories match "
                "that request.",
                "Please be more specific:"
            ]

            for memory in results:

                lines.append(
                    f"- [{memory['category']}] "
                    f"{memory['content']}"
                )

            return "\n".join(lines)

        target = results[0]

        memories = (
            self.memory.get_long_term()
        )

        target_index = None

        for index, memory in enumerate(
            memories
        ):

            if memory is target:

                target_index = index

                break

        if target_index is None:

            for index, memory in enumerate(
                memories
            ):

                if memory == target:

                    target_index = index

                    break

        if target_index is None:

            return (
                "Unable to identify the "
                "matching memory."
            )

        deleted = (
            self.memory.delete_long_term(
                target_index
            )
        )

        if not deleted:

            return (
                "Unable to forget the "
                "matching memory."
            )

        self.save_memory()

        self.security.audit.record(
            event="MEMORY_FORGOTTEN",
            action="forget",
            resource="long_term_memory",
            result="success"
        )

        return (
            "I have forgotten that memory: "
            f"{target['content']}"
        )

    # =================================================
    # MEMORY CATEGORY
    # =================================================

    def memory_category(
        self,
        category
    ):

        memories = (
            self.memory
            .search_by_category(
                category
            )
        )

        if not memories:

            return (
                f"No memories found "
                f"for category '{category}'."
            )

        lines = [
            f"MEMORY CATEGORY: {category}",
            "-" * (
                17 + len(category)
            )
        ]

        for memory in memories:

            lines.append(
                f"- {memory['content']}"
            )

        return "\n".join(lines)

    # =================================================
    # MEMORY STATUS
    # =================================================

    def memory_status(self):

        return (
            "MEMORY STATUS\n"
            "-------------\n"
            f"Short-term memories: "
            f"{self.memory.count_short_term()}\n"
            f"Long-term memories: "
            f"{self.memory.count_long_term()}\n"
            f"Persistent memory: ACTIVE"
        )

    def format_short_memory(self):

        memories = (
            self.memory.get_short_term()
        )

        if not memories:

            return (
                "Short-term memory is empty."
            )

        lines = [
            "SHORT-TERM MEMORY",
            "-----------------"
        ]

        for memory in memories:

            lines.append(
                f"- {memory['content']}"
            )

        return "\n".join(lines)

    def format_long_memory(self):

        memories = (
            self.memory.get_long_term()
        )

        if not memories:

            return (
                "Long-term memory is empty."
            )

        lines = [
            "LONG-TERM MEMORY",
            "----------------"
        ]

        for index, memory in enumerate(
            memories
        ):

            lines.append(
                f"{index}: "
                f"[{memory['category']}] "
                f"{memory['content']}"
            )

        return "\n".join(lines)

    # =================================================
    # CONVERSATION
    # =================================================

    def conversation_status(self):

        count = (
            self.conversation.message_count()
        )

        return (
            "CONVERSATION STATUS\n"
            "-------------------\n"
            f"Messages: {count}\n"
            f"Maximum messages: "
            f"{self.conversation.max_messages}\n"
            "Persistent history: ACTIVE"
        )

    # =================================================
    # PROFILE
    # =================================================

    def profile_status(self):

        profile = (
            self.profile.get_all()
        )

        if not profile:

            return (
                "USER PROFILE\n"
                "------------\n"
                "Profile is empty."
            )

        lines = [
            "USER PROFILE",
            "------------"
        ]

        for key, value in profile.items():

            lines.append(
                f"{key}: {value}"
            )

        return "\n".join(lines)

    # =================================================
    # SHUTDOWN
    # =================================================

    def shutdown(self):

        self.save_conversation()

        self.save_memory()

        self.save_profile()

        self.ui.show_message(
            "SARA is shutting down."
        )

        self.security.revoke_all_permissions()

        self.state.running = False

        self.ui.show_message(
            "All temporary permissions revoked."
        )

        self.ui.show_message(
            "SARA terminated."
        )