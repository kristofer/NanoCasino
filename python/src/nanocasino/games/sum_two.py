"""SumTwo: bet on the sum of two dice.

The payout multiplier is the profit on a winning bet (an ``ODD`` bet of $10
wins $10); a losing bet loses the stake.
"""

import random
from collections.abc import Callable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from enum import Enum
from typing import ClassVar

from nanocasino.console import Console, confirm
from nanocasino.games.base import Game
from nanocasino.player import Player
from nanocasino.wallet import CENT

QUIT = "quit"


class BetType(Enum):
    """What you can bet on. Each member knows its label, odds and win test."""

    EVEN = ("Even", 1, lambda total: total % 2 == 0)
    ODD = ("Odd", 1, lambda total: total % 2 == 1)
    EXACTLY_SEVEN = ("Exactly 7", 3, lambda total: total == 7)
    OVER_SEVEN = ("Over 7", 2, lambda total: total > 7)
    UNDER_SEVEN = ("Under 7", 2, lambda total: total < 7)

    def __init__(
        self, label: str, odds: int, predicate: Callable[[int], bool]
    ) -> None:
        self.label = label
        self.odds = odds
        self._predicate = predicate

    def wins(self, dice_total: int) -> bool:
        return self._predicate(dice_total)

    def payout(self, stake: Decimal) -> Decimal:
        """Profit on a winning bet of ``stake``."""
        return stake * self.odds


@dataclass(frozen=True)
class Bet:
    bet_type: BetType
    stake: Decimal

    def settle(self, dice_total: int) -> Decimal:
        """Net result for the player: profit if it wins, minus the stake if not."""
        if self.bet_type.wins(dice_total):
            return self.bet_type.payout(self.stake)
        return -self.stake


class SumTwo(Game):
    name: ClassVar[str] = "SumTwo"
    is_gambling: ClassVar[bool] = True

    def __init__(
        self, console: Console, player: Player, rng: random.Random | None = None
    ) -> None:
        super().__init__(console, player)
        self._rng = rng or random.Random()

    def roll_dice(self) -> int:
        """Roll two six-sided dice and return their sum."""
        return self._rng.randint(1, 6) + self._rng.randint(1, 6)

    def play(self) -> None:
        while self.player.wallet.balance > 0:
            bet_type = self._ask_bet_type()
            if bet_type is None:
                break
            bet = Bet(bet_type, self._ask_stake())
            total = self.roll_dice()
            self.console.tell(f"The roll was {total}")
            net = self._settle(bet, total)
            self.console.tell(f"You won/lost\n{net:+.2f} dollars")
            if self.player.wallet.balance > 0 and not confirm(
                self.console, "Roll again? "
            ):
                break
        else:
            self.console.tell("You're out of money!")
        self.console.tell("Thanks for playing SumTwo!\n")

    def _settle(self, bet: Bet, total: int) -> Decimal:
        net = bet.settle(total)
        wallet = self.player.wallet
        if net > 0:
            wallet.deposit(net)
        else:
            wallet.withdraw(-net)
        return net

    def _ask_bet_type(self) -> BetType | None:
        """Return the chosen bet, or ``None`` if the player quits."""
        menu = "\n".join(
            f"{number}. {bet_type.label}"
            for number, bet_type in enumerate(BetType, start=1)
        )
        choices = {str(n): bt for n, bt in enumerate(BetType, start=1)}
        while True:
            self.console.tell(f"Place a bet on one of the following:\n{menu}")
            answer = self.console.prompt("Enter your choice: ").strip().lower()
            if answer == QUIT:
                return None
            if answer in choices:
                return choices[answer]
            self.console.tell("Invalid choice. Please try again.")

    def _ask_stake(self) -> Decimal:
        while True:
            answer = self.console.prompt("Enter your bet amount: ")
            try:
                stake = Decimal(answer.strip()).quantize(CENT, ROUND_HALF_UP)
            except InvalidOperation:
                self.console.tell("Invalid amount. Please try again.")
                continue
            if not stake.is_finite() or stake <= 0:
                self.console.tell("Invalid amount. Please try again.")
            elif not self.player.wallet.can_afford(stake):
                self.console.tell("Insufficient funds. Please try again.")
            else:
                return stake
