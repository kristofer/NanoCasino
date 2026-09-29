"""CoinFlip: heads you win, tails the dealer wins."""

import random
from typing import ClassVar

from nanocasino.console import Console, confirm
from nanocasino.games.base import Game
from nanocasino.player import Player

SUSPENSE_SECONDS = 3


class CoinFlip(Game):
    name: ClassVar[str] = "CoinFlip"
    is_gambling: ClassVar[bool] = False

    def __init__(
        self, console: Console, player: Player, rng: random.Random | None = None
    ) -> None:
        super().__init__(console, player)
        self._rng = rng or random.Random()

    def flip(self) -> bool:
        """Flip the coin; ``True`` means heads."""
        return self._rng.random() < 0.5

    def play(self) -> None:
        self._introduce()
        while True:
            self.console.tell("Flipping the coin...")
            self.console.wait(SUSPENSE_SECONDS)
            heads = self.flip()
            self.console.tell(f"The coin landed on {'HEADS' if heads else 'TAILS'}")
            self.console.tell("You win!" if heads else "The dealer wins!")
            if not confirm(self.console, "Do you want to play again? (yes or no): "):
                break

    def _introduce(self) -> None:
        self.console.tell(
            "Welcome to CoinFlip\n\n"
            "The dealer will flip a coin.\n"
            "You win if the coin lands on heads.\n"
            "Good luck!\n"
        )
