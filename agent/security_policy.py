from security.permission import (
    PermissionType,
    PermissionLevel
)


class AgentSecurityPolicy:

    POLICIES = {
        "calculator": {
            "permission_type": PermissionType.CALCULATOR,
            "level": PermissionLevel.LOW
        },
        "file_write": {
            "permission_type": PermissionType.WRITE_FILE,
            "level": PermissionLevel.LOW,
            "resource_argument": "path"
        },
        "python": {
            "permission_type": PermissionType.PYTHON,
            "level": PermissionLevel.LOW
        },
        "web_search": {
            "permission_type": PermissionType.INTERNET,
            "level": PermissionLevel.MEDIUM
        },
        "application_launcher": {
            "permission_type": PermissionType.SYSTEM,
            "level": PermissionLevel.MEDIUM
        }
    }

    def get_policy(self, tool_name):

        if tool_name is None:
            return None

        tool_name = str(
            tool_name
        ).strip().lower()

        if not tool_name:
            return None

        policy = self.POLICIES.get(
            tool_name
        )

        if policy is None:
            return None

        return policy.copy()

    def get_permission_type(self, tool_name):

        policy = self.get_policy(
            tool_name
        )

        if policy is None:
            return None

        return policy.get(
            "permission_type"
        )

    def get_level(self, tool_name):

        policy = self.get_policy(
            tool_name
        )

        if policy is None:
            return None

        return policy.get(
            "level"
        )

    def get_resource(
        self,
        tool_name,
        arguments
    ):

        policy = self.get_policy(
            tool_name
        )

        if policy is None:
            return None

        if not isinstance(
            arguments,
            dict
        ):
            return None

        resource_argument = policy.get(
            "resource_argument"
        )

        if resource_argument is None:
            return None

        resource = arguments.get(
            resource_argument
        )

        if resource is None:
            return None

        resource = str(
            resource
        ).strip()

        if not resource:
            return None

        return resource