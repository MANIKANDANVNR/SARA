from pathlib import Path


class Settings:

    APP_NAME = "SARA"

    VERSION = "0.9.0"

    # -----------------------------------------
    # SYSTEM CAPABILITIES
    # -----------------------------------------

    INTERNET_ENABLED = False

    FILE_ACCESS_ENABLED = False

    SYSTEM_ACCESS_ENABLED = False

    VOICE_ENABLED = False

    AI_ENABLED = True

    # -----------------------------------------
    # DIRECTORIES
    # -----------------------------------------

    BASE_DIR = (
        Path(__file__).resolve().parent.parent
    )

    DATA_DIR = BASE_DIR / "data"

    LOG_DIR = BASE_DIR / "logs"

    MODEL_DIR = BASE_DIR / "models"

    MEMORY_DIR = DATA_DIR / "memory"

    MEMORY_FILE = (
        MEMORY_DIR / "long_term_memory.json"
    )

    CONVERSATION_FILE = (
        MEMORY_DIR / "conversation_history.json"
    )

    PROFILE_FILE = (
        MEMORY_DIR / "user_profile.json"
    )

    # -----------------------------------------
    # MEMORY
    # -----------------------------------------

    MAX_SHORT_TERM_MEMORY = 20

    MAX_CONVERSATION_MESSAGES = 20

    MAX_CONTEXT_MESSAGES = 10

    MAX_CONTEXT_MEMORIES = 5

    # -----------------------------------------
    # MEMORY CATEGORIES
    # -----------------------------------------

    MEMORY_CATEGORIES = (
        "personal",
        "preferences",
        "career",
        "projects",
        "technical",
        "general"
    )

    # -----------------------------------------
    # AI
    # -----------------------------------------

    AI_PROVIDER = "ollama"

    AI_BASE_URL = (
        "http://127.0.0.1:11434"
    )

    AI_MODEL = "qwen2.5:3b"

    AI_API_KEY = ""

    AI_TIMEOUT = 120

    AI_MAX_TOKENS = 1000

    AI_TEMPERATURE = 0.7

    # -----------------------------------------
    # SECURITY
    # -----------------------------------------

    AI_CAN_USE_TOOLS = False

    AI_CAN_ACCESS_FILES = False

    AI_CAN_ACCESS_INTERNET = False

    AI_CAN_ACCESS_SYSTEM = False

    # -----------------------------------------
    # DEBUG
    # -----------------------------------------

    DEBUG = True