from __future__ import annotations

__all__ = ("Sources",)

from .language import Language
from .consts import ROOT
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

class Sources:
    __directory: Path
    languages: dict[str, Language]

    def __init__(self) -> None:
        self.__directory = ROOT / "sources"

    @cached_property
    def languages(self) -> dict[str, Language]:
        languages = {}

        for language_directory in self.__directory.iterdir():
            if not language_directory.is_dir():
                continue

            languages[language_directory.name] = Language(language_directory)

        return languages

    def refresh(self) -> None:
        del self.languages
