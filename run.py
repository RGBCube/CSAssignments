#!/usr/bin/python3
from __future__ import annotations

from tomllib import loads as decode_toml
from dataclasses import dataclass
from functools import cached_property
from os import name as os_name, system as cmd
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chalky import Chalk

ROOT = Path(__file__).parent
IS_WIN = os_name == "nt"
QUIET_SUFFIX = " > NUL" if IS_WIN else " > /dev/null"
OS_KEY = "windows" if IS_WIN else "linux"


class Sources:
    def __init__(self) -> None:
        self.__src_dir = ROOT / "src"

    @cached_property
    def languages(self) -> dict[str, Language]:
        languages = {}

        for language_dir in self.__src_dir.iterdir():
            if not language_dir.is_dir():
                continue

            language_metadata = decode_toml((language_dir / "language.toml").read_text())
            language_metadata["directory"] = language_dir

            language = Language.from_raw(language_metadata)

            languages[language.name] = language

        return languages


@dataclass
class Colors:
    fg: Chalk
    bg: Chalk


class Language:
    def __init__(
        self,
        *,
        directory: Path,

        name: str,
        description: str,
        colors: Colors,
        build_command: str | None,
        run_command: str,
    ) -> None:
        self.__directory = directory

        self.name = name
        self.description = description
        self.colors = colors
        self.build_command = build_command
        self.run_command = run_command

    @classmethod
    def from_raw(cls, raw: dict) -> Language:
        colors = raw["colors"]

        build = raw.get("build", {})
        run = raw["run"]
        return cls(
            directory=raw["directory"],

            name=raw["name"],
            description=raw["description"],
            colors=Colors(
                fg=colors["foreground"],
                bg=colors["background"],
            ),
            build_command=build.get("common", build.get(OS_KEY)),
            run_command=run.get("common", run.get(OS_KEY)),
        )

    @property
    def assignments(self) -> dict[str, Assignment]:
        for assignment_dir in self.__directory.iterdir():
            if not assignment_dir.is_dir():
                continue

            assignment_metadata = decode_toml((assignment_dir / "assignment.toml").read_text())
            assignment_metadata["directory"] = assignment_dir
            assignment_metadata["language"] = self

            yield Assignment.from_raw(assignment_metadata)


class Assignment:
    def __init__(
        self,
        *,
        language: Language,
        directory: Path,

        name: str,
        date: str,
        description: str,
        directions: str,
    ) -> None:
        self.language = language
        self.__directory = directory

        self.name = name
        self.date = date
        self.description = description
        self.directions = directions

    @classmethod
    def from_raw(cls, raw: dict) -> Assignment:
        return cls(
            language=raw["language"],
            directory=raw["directory"],

            name=raw["name"],
            date=raw["date"],
            description=raw["description"],
            directions=raw["directions"],
        )

    def compile(self, *, quiet: bool = False) -> bool | None:
        """None = not a compiled language"""
        if self.language.build_command is None:
            return None

        return cmd(self.language.build_command + (QUIET_SUFFIX if quiet else "")) == 0
