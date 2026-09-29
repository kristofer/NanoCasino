"""The casino's games."""

from nanocasino.games.base import Game
from nanocasino.games.coin_flip import CoinFlip
from nanocasino.games.sum_two import BetType, SumTwo
from nanocasino.games.two_card import TwoCard

DEFAULT_GAMES: tuple[type[Game], ...] = (SumTwo, TwoCard, CoinFlip)

__all__ = ["BetType", "CoinFlip", "DEFAULT_GAMES", "Game", "SumTwo", "TwoCard"]
