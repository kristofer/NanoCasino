"""Playing cards: :class:`Card`, :class:`Deck` and :class:`Hand`."""

import random
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum, IntEnum
from itertools import product


class Rank(IntEnum):
    """Card ranks; the integer value is the rank's position (ace low)."""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def points(self) -> int:
        """Face value for scoring; court cards count 10."""
        return min(self.value, 10)


class Suit(Enum):
    """Card suits, each carrying the first code point of its Unicode block."""

    SPADES = 0x1F0A0
    HEARTS = 0x1F0B0
    DIAMONDS = 0x1F0C0
    CLUBS = 0x1F0D0


@dataclass(frozen=True, slots=True)
class Card:
    """An immutable playing card.

    >>> card = Card(Rank.KING, Suit.HEARTS)
    >>> str(card)
    'King of Hearts'
    >>> card.points
    10
    """

    rank: Rank
    suit: Suit

    @property
    def points(self) -> int:
        return self.rank.points

    @property
    def glyph(self) -> str:
        """The Unicode playing-card character, e.g. 🂮."""
        offset = self.rank.value
        if offset >= Rank.QUEEN:
            offset += 1  # Unicode inserts a "Knight" between Jack and Queen.
        return chr(self.suit.value + offset)

    def __str__(self) -> str:
        return f"{self.rank.name.title()} of {self.suit.name.title()}"


class EmptyDeckError(IndexError):
    """Raised when drawing from a deck with no cards left."""


class Deck:
    """A shuffled 52-card deck.

    Pass a seeded :class:`random.Random` for reproducible shuffles.
    """

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()
        self._cards = [Card(r, s) for s, r in product(Suit, Rank)]
        self.shuffle()

    def shuffle(self) -> None:
        self._rng.shuffle(self._cards)

    def draw(self) -> Card:
        if not self._cards:
            raise EmptyDeckError("the deck is empty")
        return self._cards.pop()

    def __len__(self) -> int:
        return len(self._cards)


class Hand:
    """The cards a player is holding."""

    def __init__(self, cards: Iterator[Card] | list[Card] = ()) -> None:
        self._cards = list(cards)

    def add(self, card: Card) -> None:
        self._cards.append(card)

    def pop(self, index: int = 0) -> Card:
        """Remove and return a card (the oldest by default)."""
        return self._cards.pop(index)

    def clear(self) -> None:
        self._cards.clear()

    @property
    def total(self) -> int:
        return sum(card.points for card in self._cards)

    def __len__(self) -> int:
        return len(self._cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self._cards)

    def __str__(self) -> str:
        names = "; ".join(map(str, self._cards))
        glyphs = " ".join(card.glyph for card in self._cards)
        return f"{names} {glyphs}".strip()
