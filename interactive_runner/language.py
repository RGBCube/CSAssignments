from __future__ import annotations

__all__ = ("Language",)

from functools import cached_property
from tomllib import loads as decode_toml
from typing import TYPE_CHECKING, TypedDict

from .assignment import Assignment
from .constants import OS
from .helpers import chalk_from_int, command_exists

if TYPE_CHECKING:
    from pathlib import Path


class DependencyConfig(TypedDict):
    """The list of commands that it needs."""
    common: list[str] | None
    unix: list[str] | None
    windows: list[str] | None


class RunConfig(TypedDict):
    """command.format(main_file)"""
    common: str | None
    unix: str | None
    windows: str | None


class BuildConfig(TypedDict):
    """command.format(out=out_file, main=main_file)"""
    common: str | None
    unix: str | None
    windows: str | None


class ColorConfig(TypedDict):
    foreground: int
    background: int


class LanguageConfig(TypedDict):
    name: str
    description: str
    color: ColorConfig
    build: BuildConfig | None
    run: RunConfig
    dependency: DependencyConfig | None


class Language:
    __directory: Path
    __config: LanguageConfig
    __dependencies: list[str] | None
    _build_command: str | None
    _run_command: str
    name: str
    styled_name: str
    description: str
    is_compiled: bool
    assignments: dict[str, Assignment]

    def __init__(self, directory: Path, /) -> None:
        self.__directory = directory

    @cached_property
    def __config(self) -> LanguageConfig:
        return decode_toml((self.__directory / "language.toml").read_text())

    def refresh(self) -> None:
        """TODO"""

    @property
    def name(self) -> str:
        return self.__config["name"]

    @property
    def styled_name(self) -> str:
        color = self.__config["color"]
        return chalk_from_int(color["foreground"], color["background"]) | self.name

    @property
    def description(self) -> str:
        return self.__config["description"]

    @property
    def __dependencies(self) -> list[str] | None:
        dependency = self.__config.get("dependency", {})
        return dependency.get("common") or dependency[OS]

    def check_if_dependencies_are_installed(self) -> list[str]:
        """Return value is the not installed dependencies"""
        if self.__dependencies is None:
            return []

        return [d for d in self.__dependencies if not command_exists(d)]

    @property
    def _build_command(self) -> str | None:
        build = self.__config.get("build", {})
        return build.get("common") or build.get(OS)

    @property
    def is_compiled(self) -> bool:
        return bool(self._build_command)

    @property
    def _run_command(self) -> str:
        run = self.__config["run"]
        return run.get("common") or run[OS]

    @cached_property
    def assignments(self) -> dict[str, Assignment]:
        assignments = {}

        for assignment_directory in self.__directory.iterdir():
            if not assignment_directory.is_dir():
                continue

            assignments[assignment_directory.name] = Assignment(assignment_directory, self)

        return assignments
