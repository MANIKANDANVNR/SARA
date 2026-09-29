from dataclasses import dataclass


@dataclass
class SaraState:

    running: bool = True

    authenticated: bool = False

    internet_access: bool = False
    file_access: bool = False
    system_access: bool = False
    voice_access: bool = False

    ai_available: bool = False

    emergency_shutdown: bool = False