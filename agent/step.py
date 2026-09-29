from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentStep:

    tool_name: str

    arguments: Dict[str, Any]

    status: str = "pending"

    result: Optional[Any] = None

    error: Optional[str] = None

    attempts: int = 0