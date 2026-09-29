import platform
import sys


class SystemInfoTool:

    name = "system_info"

    description = (
        "Provides safe information about the local computer "
        "and Python environment."
    )

    def execute(self):

        return {
            "operating_system": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": sys.version.split()[0],
            "architecture": platform.architecture()[0]
        }