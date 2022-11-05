from __future__ import annotations

__all__ = ("Assignment",)

from functools import cached_property
from typing import TypedDict, TYPE_CHECKING
from tomllib import loads as decode_toml
from os import system as cmd

if TYPE_CHECKING:
    from .language import Language

AssignmentConfig = TypedDict(
    "AssignmentConfig",
    {
        "name": str,
        "given-date": str,
        "main-file": str,
        "description": str,
        "directions": str,
    }
)

class Assignment:
    __config: AssignmentConfig
    language: Language
    name: str
    given_date: str
    __main_file: str
    description: str
    directions: str

    def __init__(self, directory: Path, language: Language) -> None:
        self.__directory = directory
        self.language = language

    @cached_property
    def __config(self) -> AssignmentConfig:
        return decode_toml((self.__directory / "assignment.toml").read_text())

    def refresh(self) -> None:
        del self.__config

    @property
    def name(self) -> str:
        return self.__config["name"]

    @property
    def given_date(self) -> str:
        return self.__config["given-date"]

    @property
    def __main_file(self) -> Path:
        return self.__directory / self.__config["main-file"]

    @property
    def description(self) -> str:
        return self.__config["description"]

    @property
    def directions(self) -> str:
        return self.__config["directions"]

    def compile(self, *, quiet: bool) -> int | None:
        if missing := self.language.check_dependencies_installed():
            raise ValueError(f"Needed depencencies are not installed: {', '.join(missing)}")

        if not self.language.is_compiled:
            return None

        return cmd(self.language._build_command.format(
    **{
    "out-file": self.__directory / "compiled.out",
    "main-file": self.__main_file.absolute(),
    }
    ) +
    (QUIET_SUFFIX if quiet else "")
    )

    def run(self) -> int:
        if self.language.is_compiled and not (self.__directory / "compiled.out").exists():
            self.compile(quiet=True)

        return cmd(self.language._run_command.format((self.__directory / "compiled.out").absolute() if self.language.is_compiled else self.__main_file.absolute()))

