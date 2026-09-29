"""The contract every game fulfils."""

from abc import ABC, abstractmethod
from typing import ClassVar

from nanocasino.console import Console
from nanocasino.player import Player


class Game(ABC):
    """Base class for casino games.

    Subclasses set ``name`` and ``is_gambling`` as class attributes and
    implement :meth:`play`. The casino builds its menu from these, so adding
    a game means writing a subclass and listing it; nothing else changes.
    """

    name: ClassVar[str]
    is_gambling: ClassVar[bool]

    def __init__(self, console: Console, player: Player) -> None:
        self.console = console
        self.player = player

    @abstractmethod
    def play(self) -> None:
        """Run the game until the player is done."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}(player={self.player.name!r})"
