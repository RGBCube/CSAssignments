__all__ = ("ROOT", "IS_WINDOWS", "QUIET_SUFFIX", "CHECK_COMMAND_EXISTS", "OS_KEY")

from os import name as os_name
from pathlib import Path

ROOT = Path(__file__).parent.parent
IS_WINDOWS = os_name == "nt"
QUIET_SUFFIX = " | Out-Null" if IS_WINDOWS else " > /dev/null"
CHECK_COMMAND_EXISTS = ("Get-Command {}" if IS_WINDOWS else "command -v {}") + QUIET_SUFFIX
OS_KEY = "windows" if IS_WINDOWS else "unix"
