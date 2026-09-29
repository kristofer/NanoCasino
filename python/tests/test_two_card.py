import pytest

from nanocasino.cards import Card, Deck, Hand, Rank, Suit
from nanocasino.games.two_card import Outcome, TwoCard, compare


def hand_of(*ranks: Rank) -> Hand:
    return Hand(Card(rank, Suit.SPADES) for rank in ranks)


class TestCompare:
    def test_player_wins_with_higher_total(self):
        assert compare(hand_of(Rank.KING, Rank.NINE), hand_of(Rank.TEN, Rank.TWO)) is Outcome.PLAYER

    def test_dealer_wins_with_higher_total(self):
        assert compare(hand_of(Rank.TWO, Rank.THREE), hand_of(Rank.TEN, Rank.TWO)) is Outcome.DEALER

    def test_tie(self):
        assert compare(hand_of(Rank.KING, Rank.TWO), hand_of(Rank.TEN, Rank.TWO)) is Outcome.TIE


class TestTwoCard:
    def test_metadata(self):
        assert TwoCard.name == "TwoCardStud"
        assert TwoCard.is_gambling is False

    def test_deal_gives_two_cards_each(self, player, make_console, rng):
        game = TwoCard(make_console(), player, rng)
        game.deal()
        assert len(game.player_hand) == len(game.dealer_hand) == 2
        assert len(game.deck) == 48

    def test_deal_refreshes_a_depleted_deck(self, player, make_console, rng):
        game = TwoCard(make_console(), player, rng)
        for _ in range(13):  # 52 cards = exactly 13 rounds
            game.player_hand.clear()
            game.dealer_hand.clear()
            game.deal()
        assert len(game.deck) == 0
        game.player_hand.clear()
        game.dealer_hand.clear()
        game.deal()  # would raise EmptyDeckError without a refresh
        assert len(game.deck) == 48

    def _rig(self, game: TwoCard, *ranks: Rank) -> None:
        """Make the deck deal ``ranks`` in order (player, player, dealer, dealer)."""
        deck = Deck()
        deck._cards[-len(ranks):] = [Card(r, Suit.CLUBS) for r in reversed(ranks)]
        game.deck = deck

    @pytest.mark.parametrize(
        ("ranks", "expected"),
        [((Rank.KING, Rank.NINE, Rank.TWO, Rank.THREE), "You win!"),
         ((Rank.TWO, Rank.THREE, Rank.KING, Rank.NINE), "The dealer wins!"),
         ((Rank.TEN, Rank.NINE, Rank.KING, Rank.NINE), "It's a tie!")],
    )
    def test_play_announces_result(self, player, make_console, ranks, expected):
        console = make_console(["no"])
        game = TwoCard(console, player)
        self._rig(game, *ranks)
        game.play()
        assert expected in console.text

    def test_play_shows_hands_and_sums(self, player, make_console):
        console = make_console(["no"])
        game = TwoCard(console, player)
        self._rig(game, Rank.KING, Rank.NINE, Rank.TWO, Rank.THREE)
        game.play()
        assert "Your sum is: 19" in console.text
        assert "The dealer's sum is: 5" in console.text
        assert "King of Clubs" in console.text

    def test_hands_reset_between_rounds(self, player, make_console, rng):
        console = make_console(["yes", "no"])
        game = TwoCard(console, player, rng)
        game.play()
        assert len(game.player_hand) == len(game.dealer_hand) == 2
        assert console.text.count("Your sum is") == 2

    def test_survives_more_rounds_than_one_deck(self, player, make_console, rng):
        console = make_console(["yes"] * 20 + ["no"])
        TwoCard(console, player, rng).play()
        assert console.text.count("Your sum is") == 21
