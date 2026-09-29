"""NanoCasino: a tiny text-mode casino with three games."""

from nanocasino.casino import Casino
from nanocasino.player import Player
from nanocasino.wallet import InsufficientFundsError, Wallet

__all__ = ["Casino", "InsufficientFundsError", "Player", "Wallet"]
__version__ = "1.0.0"
