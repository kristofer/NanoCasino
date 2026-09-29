"""Shared fixtures: a scripted console and seeded randomness."""

import random
from collections.abc import Iterable

import pytest

from nanocasino.player import Player


class ScriptedConsole:
    """A Console that replays canned answers and records everything shown."""

    def __init__(self, answers: Iterable[str] = ()) -> None:
        self._answers = iter(answers)
        self.output: list[str] = []
        self.prompts: list[str] = []
        self.waits: list[float] = []

    def tell(self, message: str) -> None:
        self.output.append(message)

    def prompt(self, message: str) -> str:
        self.prompts.append(message)
        try:
            return next(self._answers)
        except StopIteration:
            raise EOFError("script ran out of answers") from None

    def wait(self, seconds: float) -> None:
        self.waits.append(seconds)

    @property
    def text(self) -> str:
        return "\n".join(self.output)


@pytest.fixture
def make_console():
    return ScriptedConsole


@pytest.fixture
def player() -> Player:
    return Player("Tester")


@pytest.fixture
def rng() -> random.Random:
    return random.Random(1234)
