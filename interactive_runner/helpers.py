__all__ = ("command", "chalk_from_int", "command_exists")

from subprocess import DEVNULL as NULL, call as sys_command, getstatusoutput as sys_get_out_err

from chalky import Chalk, TrueColor

from .constants import OS


def command(s: str, /, *, quiet: bool) -> int:
    return sys_command(
        s.split(" "), shell=True, **(dict(stdout=NULL, stderr=NULL, stdin=NULL) if quiet else {})
    )


def __rgb_from_int(i: int, /) -> tuple[int, int, int]:
    r = (i >> 16) & 255
    g = (i >> 8) & 255
    b = i & 255
    return r, g, b


def chalk_from_int(foreground: int, background: int = None, /) -> Chalk:
    return Chalk(
        foreground=TrueColor(*__rgb_from_int(foreground)),
        background=TrueColor(*__rgb_from_int(background)) if background else None
    )


def command_exists(s: str, /) -> bool:
    prefix = "Get-Command" if OS == "windows" else "command -v"
    return sys_get_out_err(f"{prefix} {s}")[0] == 0
