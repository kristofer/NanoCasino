"""TwoCardStud: the higher two-card total wins.

The dealer deals two cards to the player and two to the house, and both
hands are face up. Court cards count 10, aces count 1.
"""

import random
from enum import Enum, auto
from typing import ClassVar

from nanocasino.cards import Deck, Hand
from nanocasino.console import Console, confirm
from nanocasino.games.base import Game
from nanocasino.player import Player

CARDS_PER_ROUND = 4


class Outcome(Enum):
    PLAYER = auto()
    DEALER = auto()
    TIE = auto()


def compare(player_hand: Hand, dealer_hand: Hand) -> Outcome:
    """Decide who won a round by comparing hand totals."""
    if player_hand.total > dealer_hand.total:
        return Outcome.PLAYER
    if player_hand.total < dealer_hand.total:
        return Outcome.DEALER
    return Outcome.TIE


class TwoCard(Game):
    name: ClassVar[str] = "TwoCardStud"
    is_gambling: ClassVar[bool] = False

    def __init__(
        self, console: Console, player: Player, rng: random.Random | None = None
    ) -> None:
        super().__init__(console, player)
        self._rng = rng
        self.deck = Deck(rng)
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def deal(self) -> None:
        """Deal two cards each, starting over with a fresh deck if it runs low."""
        if len(self.deck) < CARDS_PER_ROUND:
            self.deck = Deck(self._rng)
        for hand in (self.player_hand, self.dealer_hand):
            hand.add(self.deck.draw())
            hand.add(self.deck.draw())

    def play(self) -> None:
        tell = self.console.tell
        tell(
            "Welcome to TwoCardStud\n\n"
            "The dealer will deal two cards to you and two cards to the house.\n"
            "You win if the sum of your two cards is higher than the dealer's.\n"
            "Good luck!\n"
        )
        while True:
            self.player_hand.clear()
            self.dealer_hand.clear()
            self.deal()
            tell(f"Your Hand: [{self.player_hand}]")
            tell(f"Dealer   : [{self.dealer_hand}]")
            tell(f"Your sum is: {self.player_hand.total}")
            tell(f"The dealer's sum is: {self.dealer_hand.total}")
            tell(self._verdict(compare(self.player_hand, self.dealer_hand)))
            if not confirm(self.console, "Do you wish to play again? (yes or no)"):
                break

    @staticmethod
    def _verdict(outcome: Outcome) -> str:
        return {
            Outcome.PLAYER: "You win!",
            Outcome.DEALER: "The dealer wins!",
            Outcome.TIE: "It's a tie!",
        }[outcome]
