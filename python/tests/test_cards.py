import random
from dataclasses import FrozenInstanceError

import pytest

from nanocasino.cards import Card, Deck, EmptyDeckError, Hand, Rank, Suit


class TestCard:
    def test_fields(self):
        card = Card(Rank.ACE, Suit.SPADES)
        assert card.rank is Rank.ACE
        assert card.suit is Suit.SPADES

    def test_str(self):
        assert str(Card(Rank.KING, Suit.HEARTS)) == "King of Hearts"

    def test_is_immutable_and_hashable(self):
        card = Card(Rank.TWO, Suit.CLUBS)
        with pytest.raises(FrozenInstanceError):
            card.rank = Rank.THREE
        assert card == Card(Rank.TWO, Suit.CLUBS)
        assert len({card, Card(Rank.TWO, Suit.CLUBS)}) == 1

    @pytest.mark.parametrize(
        ("rank", "points"),
        [(Rank.ACE, 1), (Rank.TWO, 2), (Rank.NINE, 9), (Rank.TEN, 10),
         (Rank.JACK, 10), (Rank.QUEEN, 10), (Rank.KING, 10)],
    )
    def test_points(self, rank, points):
        assert Card(rank, Suit.CLUBS).points == points

    @pytest.mark.parametrize(
        ("rank", "suit", "glyph"),
        [(Rank.ACE, Suit.SPADES, "\U0001F0A1"),
         (Rank.TEN, Suit.HEARTS, "\U0001F0BA"),
         (Rank.JACK, Suit.DIAMONDS, "\U0001F0CB"),
         (Rank.QUEEN, Suit.CLUBS, "\U0001F0DD"),  # skips the Knight at ...DC
         (Rank.KING, Suit.SPADES, "\U0001F0AE")],
    )
    def test_glyph(self, rank, suit, glyph):
        assert Card(rank, suit).glyph == glyph

    def test_every_card_has_a_distinct_glyph(self):
        glyphs = {Card(r, s).glyph for r in Rank for s in Suit}
        assert len(glyphs) == 52


class TestDeck:
    def test_has_52_unique_cards(self):
        deck = Deck()
        cards = [deck.draw() for _ in range(52)]
        assert len(set(cards)) == 52

    def test_draw_shrinks_deck(self):
        deck = Deck()
        deck.draw()
        assert len(deck) == 51

    def test_drawing_from_empty_deck_raises(self):
        deck = Deck()
        for _ in range(52):
            deck.draw()
        with pytest.raises(EmptyDeckError):
            deck.draw()

    def test_same_seed_same_order(self):
        a, b = Deck(random.Random(7)), Deck(random.Random(7))
        assert [a.draw() for _ in range(52)] == [b.draw() for _ in range(52)]

    def test_different_seeds_differ(self):
        a, b = Deck(random.Random(1)), Deck(random.Random(2))
        assert [a.draw() for _ in range(52)] != [b.draw() for _ in range(52)]

    def test_shuffle_keeps_the_same_cards(self):
        deck = Deck(random.Random(3))
        deck.shuffle()
        assert len(deck) == 52
        assert len({deck.draw() for _ in range(52)}) == 52


class TestHand:
    @pytest.fixture
    def cards(self):
        return Card(Rank.ACE, Suit.SPADES), Card(Rank.KING, Suit.HEARTS)

    def test_add_and_len(self, cards):
        hand = Hand()
        assert len(hand) == 0
        for i, card in enumerate(cards, 1):
            hand.add(card)
            assert len(hand) == i

    def test_pop_takes_oldest_by_default(self, cards):
        hand = Hand(cards)
        assert hand.pop() == cards[0]
        assert len(hand) == 1

    def test_pop_by_index(self, cards):
        assert Hand(cards).pop(1) == cards[1]

    def test_pop_empty_raises(self):
        with pytest.raises(IndexError):
            Hand().pop()

    def test_total(self, cards):
        assert Hand(cards).total == 11
        assert Hand().total == 0

    def test_clear(self, cards):
        hand = Hand(cards)
        hand.clear()
        assert len(hand) == 0

    def test_iterates_in_order(self, cards):
        assert list(Hand(cards)) == list(cards)

    def test_str_lists_names_and_glyphs(self, cards):
        text = str(Hand(cards))
        assert "Ace of Spades; King of Hearts" in text
        assert cards[0].glyph in text and cards[1].glyph in text

    def test_str_empty(self):
        assert str(Hand()) == ""
