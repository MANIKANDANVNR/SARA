from enum import Enum


class AuthenticationLevel(Enum):

    NONE = 0
    BASIC = 1
    STRONG = 2
    CRITICAL = 3


class AuthenticationManager:

    def __init__(self, state):

        self.state = state

        self.current_level = (
            AuthenticationLevel.NONE
        )

    # =================================================
    # BASIC AUTHENTICATION
    # =================================================

    def authenticate_basic(self):

        # Temporary development authentication.
        # Real PIN/passkey authentication will be
        # implemented in a later security phase.

        self.state.authenticated = True

        self.current_level = (
            AuthenticationLevel.BASIC
        )

        return True

    # =================================================
    # STRONG AUTHENTICATION
    # =================================================

    def authenticate_strong(self):

        if not self.state.authenticated:

            return False

        self.current_level = (
            AuthenticationLevel.STRONG
        )

        return True

    # =================================================
    # CRITICAL AUTHENTICATION
    # =================================================

    def authenticate_critical(self):

        if not self.state.authenticated:

            return False

        self.current_level = (
            AuthenticationLevel.CRITICAL
        )

        return True

    # =================================================
    # CHECK AUTHENTICATION LEVEL
    # =================================================

    def has_level(self, required_level):

        return (
            self.current_level.value
            >= required_level.value
        )

    # =================================================
    # LOGOUT
    # =================================================

    def logout(self):

        self.state.authenticated = False

        self.current_level = (
            AuthenticationLevel.NONE
        )