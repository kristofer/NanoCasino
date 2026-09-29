"""Money handling.

Amounts are :class:`~decimal.Decimal` so that cents never drift the way
binary floats do (``0.1 + 0.2 != 0.3``).
"""

from dataclasses import dataclass
from decimal import Decimal

CENT = Decimal("0.01")


class InsufficientFundsError(ValueError):
    """Raised when a withdrawal exceeds the wallet's balance."""


@dataclass
class Wallet:
    """A player's money.

    >>> wallet = Wallet("kris", Decimal("100"))
    >>> wallet.withdraw(Decimal("30"))
    >>> str(wallet)
    '$70.00'
    """

    account_id: str
    balance: Decimal = Decimal("500")

    def __post_init__(self) -> None:
        self.balance = Decimal(self.balance)

    def deposit(self, amount: Decimal) -> None:
        self._require_positive(amount)
        self.balance += amount

    def withdraw(self, amount: Decimal) -> None:
        self._require_positive(amount)
        if amount > self.balance:
            raise InsufficientFundsError(
                f"cannot withdraw {amount:.2f}; balance is {self.balance:.2f}"
            )
        self.balance -= amount

    def can_afford(self, amount: Decimal) -> bool:
        return amount <= self.balance

    def __str__(self) -> str:
        return f"${self.balance:,.2f}"

    @staticmethod
    def _require_positive(amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError(f"amount must be positive, got {amount}")
