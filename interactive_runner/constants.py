__all__ = ("ROOT", "OS")

from os import name as os_name
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).parent.parent
OS: Literal["windows"] | Literal["unix"] = "windows" if os_name == "nt" else "unix"  # type: ignore
