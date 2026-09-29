from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional


class PermissionType(Enum):

    READ_FILE = "read_file"

    WRITE_FILE = "write_file"

    INTERNET = "internet"

    SYSTEM = "system"

    PYTHON = "python"

    MICROPHONE = "microphone"

    SPEAKER = "speaker"

    CAMERA = "camera"

    CALCULATOR = "calculator"


class PermissionLevel(Enum):

    LOW = 1

    MEDIUM = 2

    HIGH = 3

    CRITICAL = 4


@dataclass
class Permission:

    permission_type: PermissionType

    level: PermissionLevel

    resource: Optional[str] = None

    expires_at: Optional[datetime] = None

    approved: bool = False

    def is_valid(self):

        if not self.approved:

            return False

        if self.expires_at is None:

            return True

        return datetime.now() < self.expires_at

    def expires_in(self, seconds):

        self.expires_at = (
            datetime.now()
            + timedelta(seconds=seconds)
        )