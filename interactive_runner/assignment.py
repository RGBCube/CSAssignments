from __future__ import annotations

__all__ = ("Assignment",)

from functools import cached_property
from tomllib import loads as decode_toml
from typing import TYPE_CHECKING, TypedDict

from .helpers import command

if TYPE_CHECKING:
    from pathlib import Path
    from .language import Language


class AssignmentConfig(TypedDict):
    name: str
    date: str
    main: str
    description: str
    directions: str


class Assignment:
    __config: AssignmentConfig
    __main: str
    language: Language
    name: str
    date: str
    description: str
    directions: str

    def __init__(self, directory: Path, language: Language, /) -> None:
        self.__directory = directory
        self.language = language

    @cached_property
    def __config(self) -> AssignmentConfig:
        return decode_toml((self.__directory / "assignment.toml").read_text())

    def refresh(self) -> None:
        """TODO"""

    @property
    def name(self) -> str:
        return self.__config["name"]

    @property
    def date(self) -> str:
        return self.__config["date"]

    @property
    def __main(self) -> Path:
        return (self.__directory / self.__config["main"]).absolute()

    @property
    def __out(self) -> Path:
        return (self.__directory / "compiled.out").absolute()

    @property
    def description(self) -> str:
        return self.__config["description"]

    @property
    def directions(self) -> str:
        return self.__config["directions"]

    def compile(self, *, quiet: bool) -> int | None:
        if missing := self.language.check_if_dependencies_are_installed():
            raise ValueError(
                f"Some dependencies that are needed are not installed: {', '.join(missing)}"
            )

        if not self.language.is_compiled:
            return None

        return command(
            self.language._build_command.format(
                out=self.__out,
                main=self.__main
            ),
            quiet=quiet
        )

    def run(self) -> int:
        if self.language.is_compiled and not (self.__directory / "compiled.out").exists():
            self.compile(quiet=True)

        return command(
            self.language._run_command.format(
                self.__out if self.language.is_compiled else self.__main
            ),
            quiet=False
        )
