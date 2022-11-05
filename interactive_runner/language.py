from __future__ import annotations

__all__ = ("Language",)

from .assignment import Assignment
from .consts import OS_KEY, CHECK_COMMAND_EXISTS
from typing import TYPE_CHECKING, TypedDict
from tomllib import loads as decode_toml
from chalky import hex
from functools import cached_property
from os import system as cmd
from chalky.shortcuts.sty import bold

if TYPE_CHECKING:
    from pathlib import Path

LanguageConfig = TypedDict(
    "LanguageConfig",
    {
        "name": str,
        "descripton": str,
        "colors": TypedDict(
            "ColorConfig",
            {
                "foregroud": int,
                "background": int,
            }
        ),
        "build": None | TypedDict(
            "BuildConfig",
            {
                "common": str | None,
                "unix": str | None,
                "windows": str | None,
            }
        ),
        "run": TypedDict(
            "RunConfig",
            {
                "common": str | None,
                "unix": str | None,
                "windows": str | None,
            }
        ),
        "dependencies": None | TypedDict(
            "DependencyConfig",
            {
                "common": list[str] | None,
                "unix": list[str] | None,
                "windows": list[str] | None,
            }
        ),
    }
)

class Language:
    __directory: Path
    __config: LanguageConfig
    name: str
    styled_name: str
    description: str
    __dependencies: list[str] | None
    _build_command: str | None
    is_compiled: bool
    _run_command: str
    assignments: dict[str, Assignment]

    def __init__(self, directory: Path) -> None:
        self.__directory = directory

    @cached_property
    def __config(self) -> LanguageConfig:
        return decode_toml((self.__directory / "language.toml").read_text())

    def refresh(self) -> None:
        del self.__config
        del self.assignments

    @property
    def name(self) -> str:
        return self.__config["name"]

    @property
    def styled_name(self) -> str:
        colors = self.__config["colors"]
        # hack
        return hex(colors["foreground"]) & hex(colors["background"], background=True) | self.name

    @property
    def description(self) -> str:
        return self.__config["description"]

    @property
    def __dependencies(self) -> list[str] | None:
        dependencies = self.__config.get("dependencies", {})
        return dependencies.get("common", dependencies.get(OS_KEY))

    def check_dependencies_installed(self) -> list[str]:
        if self.__dependencies is None:
            return []

        not_installed = []
        for dependency in self.__dependencies:
            exit = cmd(CHECK_COMMAND_EXISTS.format(dependency))

            if exit:
                not_installed.append(dependency)

        return not_installed

    @property
    def _build_command(self) -> str | None:
        build = self.__config.get("build", {})
        return build.get("common", build.get(OS_KEY))

    @property
    def is_compiled(self) -> bool:
        return bool(self._build_command)

    @property
    def _run_command(self) -> str:
        run = self.__config["run"]
        return run.get("common", run.get(OS_KEY))

    @cached_property
    def assignments(self) -> dict[str, Assignment]:
        assignments = {}

        for assignment_directory in self.__directory.iterdir():
            if not assignment_directory.is_dir():
                continue

            assignments[assignment_directory.name] = Assignment(assignment_directory, self)

        return assignments
