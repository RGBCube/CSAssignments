from typing import Literal, overload

from chalky.shortcuts.sty import bold

from . import Sources
from .helpers import chalk_from_int as color

__print = print
__input = input
__int = int

green = color(0x39ff14)
red = color(0xff0000)

invalid_input = red | "Invalid input! Try again."

sources = Sources()


def print(*s: str, nl: bool = False) -> None:
    __print(*s)
    if nl:
        __print()


@overload
def input(
    *s: str,
    nl: bool = False,
    int: bool = Literal[True],
    valid: set[int] | None = None
) -> int:
    ...


@overload
def input(*s: str, nl: bool = False) -> str:
    ...


def input(*s: str, nl: bool = False, int: bool = False, valid: set[int] | None = None) -> str | int:
    r = __input(*s).lower().strip()
    if r == "exit":
        print(red | "Exiting...")
        exit()
    elif int:
        try:
            val = __int(r)
            if valid and val not in valid:
                print(invalid_input)
                val = input(*s, int=int, valid=valid)
            if nl:
                print()
        except ValueError:
            print(invalid_input)
            val = input(*s, int=int, valid=valid)
        finally:
            return val
    else:
        if nl:
            print()
        return r


while True:
    print("----------", green & bold | "MAIN MENU", "----------")
    print(f"{green | 1}: Browse languages.")
    print(f"{green | 2}: Invalidate all cache.", nl=True)

    choice = input("Choose an option by its number: ", nl=True, int=True, valid={1, 2})

    match choice:
        case 1:
            ...

        case 2:
            sources.refresh()
            print(green | "Successfully invalidated all cache.", nl=True)
