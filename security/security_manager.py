from security.permission import (
    Permission,
    PermissionType,
    PermissionLevel
)

from security.authentication import (
    AuthenticationManager,
    AuthenticationLevel
)

from security.audit import AuditLogger

from security.confirmation import (
    ConfirmationManager
)


class SecurityManager:

    def __init__(self, state):

        self.state = state

        self.authentication = (
            AuthenticationManager(state)
        )

        self.audit = AuditLogger()

        self.confirmation = (
            ConfirmationManager()
        )

        self.permissions = []

    # =================================================
    # AUTHENTICATION
    # =================================================

    def authenticate(self):

        result = (
            self.authentication
            .authenticate_basic()
        )

        self.audit.record(
            event="AUTHENTICATION",
            result=(
                "SUCCESS"
                if result
                else "FAILED"
            )
        )

        return result

    def authenticate_strong(self):

        result = (
            self.authentication
            .authenticate_strong()
        )

        self.audit.record(
            event="STRONG_AUTHENTICATION",
            result=(
                "SUCCESS"
                if result
                else "FAILED"
            )
        )

        return result

    def authenticate_critical(self):

        result = (
            self.authentication
            .authenticate_critical()
        )

        self.audit.record(
            event="CRITICAL_AUTHENTICATION",
            result=(
                "SUCCESS"
                if result
                else "FAILED"
            )
        )

        return result

    def logout(self):

        self.authentication.logout()

        self.revoke_all_permissions()

        self.audit.record(
            event="LOGOUT",
            result="SUCCESS"
        )

    def is_authenticated(self):

        return self.state.authenticated

    # =================================================
    # AUTHENTICATION REQUIREMENT
    # =================================================

    def authentication_level_sufficient(
        self,
        permission_level
    ):

        required_level = (
            AuthenticationLevel.BASIC
        )

        if permission_level == (
            PermissionLevel.LOW
        ):

            required_level = (
                AuthenticationLevel.BASIC
            )

        elif permission_level == (
            PermissionLevel.MEDIUM
        ):

            required_level = (
                AuthenticationLevel.STRONG
            )

        elif permission_level == (
            PermissionLevel.HIGH
        ):

            required_level = (
                AuthenticationLevel.CRITICAL
            )

        elif permission_level == (
            PermissionLevel.CRITICAL
        ):

            required_level = (
                AuthenticationLevel.CRITICAL
            )

        return (
            self.authentication.has_level(
                required_level
            )
        )

    # =================================================
    # PERMISSIONS
    # =================================================

    def request_permission(
        self,
        permission_type,
        level,
        resource=None,
        duration=None
    ):

        # -------------------------------------------------
        # FAIL CLOSED: AUTHENTICATION
        # -------------------------------------------------

        if not self.is_authenticated():

            self.audit.record(
                event="PERMISSION_DENIED",
                action=permission_type.value,
                resource=resource,
                result="NOT_AUTHENTICATED"
            )

            return False

        # -------------------------------------------------
        # FILE RESOURCE MUST BE EXPLICIT
        # -------------------------------------------------

        if permission_type in {
            PermissionType.READ_FILE,
            PermissionType.WRITE_FILE
        }:

            if not resource:

                self.audit.record(
                    event="PERMISSION_DENIED",
                    action=permission_type.value,
                    resource=resource,
                    result="RESOURCE_REQUIRED"
                )

                return False

        # -------------------------------------------------
        # AUTHENTICATION LEVEL
        # -------------------------------------------------

        if not self.authentication_level_sufficient(
            level
        ):

            self.audit.record(
                event="PERMISSION_DENIED",
                action=permission_type.value,
                resource=resource,
                result="INSUFFICIENT_AUTHENTICATION"
            )

            return False

        # -------------------------------------------------
        # CREATE PERMISSION
        # -------------------------------------------------

        if resource is not None:

            resource = str(
                resource
            ).strip()

            if not resource:
                self.audit.record(
                    event="PERMISSION_DENIED",
                    action=permission_type.value,
                    resource=resource,
                    result="RESOURCE_REQUIRED"
                )

                return False

        permission = Permission(
            permission_type=permission_type,
            level=level,
            resource=resource,
            approved=False
        )

        # -------------------------------------------------
        # HIGH / CRITICAL CONFIRMATION
        # -------------------------------------------------

        if level in {
            PermissionLevel.HIGH,
            PermissionLevel.CRITICAL
        }:

            confirmed = (
                self.confirmation
                .request_confirmation(
                    f"Permission requested: "
                    f"{permission_type.value}\n"
                    f"Resource: {resource}"
                )
            )

            if not confirmed:

                self.audit.record(
                    event="PERMISSION_DENIED",
                    action=permission_type.value,
                    resource=resource,
                    result="USER_DENIED"
                )

                return False

        # -------------------------------------------------
        # APPROVE
        # -------------------------------------------------

        permission.approved = True

        if duration is not None:

            permission.expires_in(duration)

        self.permissions.append(permission)

        self.audit.record(
            event="PERMISSION_GRANTED",
            action=permission_type.value,
            resource=resource,
            result="GRANTED"
        )

        return True

    # =================================================
    # CHECK PERMISSION
    # =================================================

    def has_permission(
        self,
        permission_type,
        resource=None
    ):

        if not self.is_authenticated():

            return False

        # File permissions must always be
        # checked against an exact resource.

        if permission_type in {
            PermissionType.READ_FILE,
            PermissionType.WRITE_FILE
        }:

            if not resource:

                return False

        for permission in self.permissions:

            if not permission.is_valid():

                continue

            if permission.permission_type != (
                permission_type
            ):

                continue

            # -------------------------------------------------
            # FILE ACCESS = EXACT RESOURCE MATCH
            # -------------------------------------------------

            if permission_type in {
                PermissionType.READ_FILE,
                PermissionType.WRITE_FILE
            }:

                if permission.resource != resource:

                    continue

                return True

            # -------------------------------------------------
            # OTHER PERMISSIONS
            # -------------------------------------------------

            if permission.resource is not None:

                if resource != permission.resource:

                    continue

            return True

        return False

    # =================================================
    # REVOKE ONE PERMISSION
    # =================================================

    def revoke_permission(
        self,
        permission_type,
        resource=None
    ):

        remaining = []

        for permission in self.permissions:

            if (
                permission.permission_type
                == permission_type
                and
                (
                    resource is None
                    or permission.resource == resource
                )
            ):

                self.audit.record(
                    event="PERMISSION_REVOKED",
                    action=permission_type.value,
                    resource=resource,
                    result="REVOKED"
                )

                continue

            remaining.append(permission)

        self.permissions = remaining

    # =================================================
    # REVOKE ALL
    # =================================================

    def revoke_all_permissions(self):

        self.permissions.clear()

        self.audit.record(
            event="ALL_PERMISSIONS_REVOKED",
            result="SUCCESS"
        )

    # =================================================
    # EMERGENCY SHUTDOWN
    # =================================================

    def emergency_shutdown(self):

        self.state.emergency_shutdown = True

        self.revoke_all_permissions()

        self.authentication.logout()

        self.state.running = False

        self.audit.record(
            event="EMERGENCY_SHUTDOWN",
            result="ACTIVATED"
        )

    # =================================================
    # SECURITY STATUS
    # =================================================

    def get_security_status(self):

        active_permissions = []

        for permission in self.permissions:

            if permission.is_valid():

                active_permissions.append(
                    permission.permission_type.value
                )

        return {

            "authenticated":
                self.is_authenticated(),

            "authentication_level":
                self.authentication.current_level.name,

            "active_permissions":
                active_permissions,

            "emergency_shutdown":
                self.state.emergency_shutdown
        }