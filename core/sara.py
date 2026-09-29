from datetime import datetime

from security.permission import (
    PermissionType,
    PermissionLevel
)


class Sara:

    def __init__(self, security):

        self.name = "SARA"

        self.version = "0.9.0"

        self.security = security

        self.commands = {
            "hello",
            "hi",
            "hey",
            "status",
            "time",
            "date",
            "help",
            "shutdown",
            "exit",
            "quit"
        }

    def process_command(self, command):

        command = command.strip()

        if not command:
            return "Please tell me what you need."

        lower = command.lower()

        if lower in {"hello", "hi", "hey"}:
            return (
                "Hello. I am SARA, "
                "your personal AI assistant."
            )

        if lower == "time":
            return datetime.now().strftime(
                "The current time is %I:%M %p."
            )

        if lower == "date":
            return datetime.now().strftime(
                "Today is %d %B %Y."
            )

        if lower == "status":
            return self.get_status()

        if lower == "security":
            return self.security_status()

        if lower == "authenticate":

            if self.security.authenticate():
                return "Basic authentication successful."

            return "Authentication failed."

        if lower == "authenticate strong":

            if self.security.authenticate_strong():
                return "Strong authentication successful."

            return (
                "Strong authentication failed. "
                "Basic authentication is required first."
            )

        if lower == "authenticate critical":

            if self.security.authenticate_critical():
                return "Critical authentication successful."

            return (
                "Critical authentication failed. "
                "Basic authentication is required first."
            )

        if lower == "logout":

            self.security.logout()

            return "You have been logged out."

        if lower == "permissions":

            return self.permission_status()

        if lower == "emergency shutdown":

            self.security.emergency_shutdown()

            return "Emergency shutdown activated."

        if lower == "help":

            return self.get_help()

        if lower in {
            "shutdown",
            "exit",
            "quit"
        }:

            return self.shutdown_command()

        return (
            "I received your request:\n"
            f'"{command}"\n\n'
            "My AI brain is not connected yet."
        )

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

    def permission_status(self):

        return self.security_status()

    def get_status(self):

        security_status = (
            self.security
            .get_security_status()
        )

        return (
            "SARA STATUS\n"
            "------------\n"
            f"Name: {self.name}\n"
            f"Version: {self.version}\n"
            "Core: ONLINE\n"
            "Security: ACTIVE\n"
            "Persistent Intelligence: ACTIVE\n"
            f"Authenticated: "
            f"{security_status['authenticated']}\n"
            "AI Brain: ONLINE\n"
            "Voice: OFFLINE\n"
            "Internet: OFF\n"
            "File Access: OFF\n"
            "System Access: OFF"
        )

    def get_help(self):

        return (
            "Available commands:\n"
            "- hello\n"
            "- time\n"
            "- date\n"
            "- status\n"
            "- security\n"
            "- permissions\n"
            "- authenticate\n"
            "- authenticate strong\n"
            "- authenticate critical\n"
            "- logout\n"
            "- help\n"
            "- shutdown"
        )

    def shutdown_command(self):

        return "SARA is shutting down."
