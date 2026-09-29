from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class AgentTask:

    request: str

    status: str = "pending"

    steps: List[Any] = field(
        default_factory=list
    )

    current_step: int = 0

    result: Optional[Any] = None

    error: Optional[str] = None

    report: Optional[str] = None