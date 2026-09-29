from security.permission import (
    PermissionType,
    PermissionLevel
)


class SecurityGate:

    def __init__(self, security_manager):

        self.security = security_manager

    # =================================================
    # AUTHORIZATION CHECK
    # =================================================

    def check(
        self,
        permission_type,
        level,
        resource=None
    ):

        # -------------------------------------------------
        # PERMISSION TYPE VALIDATION
        # -------------------------------------------------

        if not isinstance(
            permission_type,
            PermissionType
        ):

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action="invalid_permission_type",
                resource=resource,
                result="INVALID_PERMISSION_TYPE"
            )

            return False

        # -------------------------------------------------
        # PERMISSION LEVEL VALIDATION
        # -------------------------------------------------

        if not isinstance(
            level,
            PermissionLevel
        ):

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="INVALID_PERMISSION_LEVEL"
            )

            return False

        # -------------------------------------------------
        # EMERGENCY SHUTDOWN
        # -------------------------------------------------

        if self.security.state.emergency_shutdown:

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="EMERGENCY_SHUTDOWN"
            )

            return False

        # -------------------------------------------------
        # AUTHENTICATION
        # -------------------------------------------------

        if not self.security.is_authenticated():

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="NOT_AUTHENTICATED"
            )

            return False

        # -------------------------------------------------
        # FILE RESOURCE VALIDATION
        # -------------------------------------------------

        if permission_type in {
            PermissionType.READ_FILE,
            PermissionType.WRITE_FILE
        }:

            if not resource:

                self.security.audit.record(
                    event="SECURITY_GATE_DENIED",
                    action=permission_type.value,
                    resource=resource,
                    result="RESOURCE_REQUIRED"
                )

                return False

        # -------------------------------------------------
        # PERMISSION CHECK
        # -------------------------------------------------

        if not self.security.has_permission(
            permission_type,
            resource=resource
        ):

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="PERMISSION_NOT_GRANTED"
            )

            return False

        # -------------------------------------------------
        # ACCESS GRANTED
        # -------------------------------------------------

        self.security.audit.record(
            event="SECURITY_GATE_ALLOWED",
            action=permission_type.value,
            resource=resource,
            result="ALLOWED"
        )

        return True

    # =================================================
    # REQUEST ACCESS
    # =================================================

    def request_access(
        self,
        permission_type,
        level,
        resource=None,
        duration=None
    ):

        # -------------------------------------------------
        # PERMISSION TYPE VALIDATION
        # -------------------------------------------------

        if not isinstance(
            permission_type,
            PermissionType
        ):

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action="invalid_permission_type",
                resource=resource,
                result="INVALID_PERMISSION_TYPE"
            )

            return False

        # -------------------------------------------------
        # PERMISSION LEVEL VALIDATION
        # -------------------------------------------------

        if not isinstance(
            level,
            PermissionLevel
        ):

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="INVALID_PERMISSION_LEVEL"
            )

            return False

        # -------------------------------------------------
        # EMERGENCY SHUTDOWN
        # -------------------------------------------------

        if self.security.state.emergency_shutdown:

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="EMERGENCY_SHUTDOWN"
            )

            return False

        # -------------------------------------------------
        # REQUEST PERMISSION THROUGH SECURITY MANAGER
        # -------------------------------------------------

        granted = (
            self.security.request_permission(
                permission_type=permission_type,
                level=level,
                resource=resource,
                duration=duration
            )
        )

        if not granted:

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action=permission_type.value,
                resource=resource,
                result="PERMISSION_REQUEST_DENIED"
            )

            return False

        # -------------------------------------------------
        # VERIFY PERMISSION
        # -------------------------------------------------

        return self.check(
            permission_type=permission_type,
            level=level,
            resource=resource
        )

    # =================================================
    # TOOL ACCESS
    # =================================================

    def authorize_tool(
        self,
        tool_name,
        permission_type,
        level,
        resource=None
    ):

        if not tool_name:

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action="tool",
                resource=None,
                result="TOOL_NAME_REQUIRED"
            )

            return False

        tool_name = str(
            tool_name
        ).strip().lower()

        if not tool_name:

            self.security.audit.record(
                event="SECURITY_GATE_DENIED",
                action="tool",
                resource=None,
                result="TOOL_NAME_REQUIRED"
            )

            return False

        allowed = self.check(
            permission_type=permission_type,
            level=level,
            resource=resource
        )

        self.security.audit.record(
            event="TOOL_AUTHORIZATION",
            action=tool_name,
            resource=resource,
            result=(
                "ALLOWED"
                if allowed
                else "DENIED"
            )
        )

        return allowed

    # =================================================
    # TOOL ACCESS REQUEST
    # =================================================

    def request_tool_access(
        self,
        tool_name,
        permission_type,
        level,
        resource=None,
        duration=None
    ):

        if not tool_name:

            self.security.audit.record(
                event="TOOL_AUTHORIZATION",
                action="tool",
                resource=resource,
                result="TOOL_NAME_REQUIRED"
            )

            return False

        tool_name = str(
            tool_name
        ).strip().lower()

        if not tool_name:

            return False

        granted = self.request_access(
            permission_type=permission_type,
            level=level,
            resource=resource,
            duration=duration
        )

        self.security.audit.record(
            event="TOOL_ACCESS_REQUEST",
            action=tool_name,
            resource=resource,
            result=(
                "GRANTED"
                if granted
                else "DENIED"
            )
        )

        return granted