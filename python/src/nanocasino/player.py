"""Players."""

from dataclasses import dataclass, field
from decimal import Decimal

from nanocasino.wallet import Wallet

STARTING_BALANCE = Decimal("500")


@dataclass
class Player:
    """A casino patron: a name and a wallet.

    Games only rely on ``name`` and ``wallet`` (duck typing), so there is no
    need for a separate interface class.
    """

    name: str
    wallet: Wallet = field(init=False)

    def __post_init__(self) -> None:
        self.wallet = Wallet(self.name, STARTING_BALANCE)
