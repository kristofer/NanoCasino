import random
from collections import Counter
from decimal import Decimal

import pytest

from nanocasino.games.sum_two import Bet, BetType, SumTwo

D = Decimal


class TestBetType:
    @pytest.mark.parametrize(
        ("bet_type", "odds"),
        [(BetType.EVEN, 1), (BetType.ODD, 1), (BetType.OVER_SEVEN, 2),
         (BetType.UNDER_SEVEN, 2), (BetType.EXACTLY_SEVEN, 3)],
    )
    def test_payout_multiplies_stake_by_odds(self, bet_type, odds):
        assert bet_type.payout(D("1")) == odds
        assert bet_type.payout(D("10.50")) == D("10.50") * odds

    @pytest.mark.parametrize(
        ("bet_type", "winners"),
        [(BetType.EVEN, {2, 4, 6, 8, 10, 12}),
         (BetType.ODD, {3, 5, 7, 9, 11}),
         (BetType.EXACTLY_SEVEN, {7}),
         (BetType.OVER_SEVEN, {8, 9, 10, 11, 12}),
         (BetType.UNDER_SEVEN, {2, 3, 4, 5, 6})],
    )
    def test_wins_exactly_on_expected_totals(self, bet_type, winners):
        assert {t for t in range(2, 13) if bet_type.wins(t)} == winners

    def test_seven_results(self):
        wins = {bt: bt.wins(7) for bt in BetType}
        assert wins == {
            BetType.EVEN: False, BetType.ODD: True, BetType.OVER_SEVEN: False,
            BetType.UNDER_SEVEN: False, BetType.EXACTLY_SEVEN: True,
        }


class TestBet:
    def test_winning_bet_settles_to_profit(self):
        assert Bet(BetType.OVER_SEVEN, D("10")).settle(9) == D("20")

    def test_losing_bet_settles_to_minus_stake(self):
        assert Bet(BetType.OVER_SEVEN, D("10")).settle(5) == D("-10")


class TestDice:
    def test_roll_stays_in_range(self, player, make_console, rng):
        game = SumTwo(make_console(), player, rng)
        assert all(2 <= game.roll_dice() <= 12 for _ in range(1000))

    def test_distribution_is_triangular(self, player, make_console):
        game = SumTwo(make_console(), player, random.Random(99))
        n = 36_000
        counts = Counter(game.roll_dice() for _ in range(n))
        for total in range(2, 13):
            expected = n * (6 - abs(total - 7)) / 36
            assert counts[total] == pytest.approx(expected, rel=0.1)

    def test_seeded_rolls_are_reproducible(self, player, make_console):
        a = SumTwo(make_console(), player, random.Random(5))
        b = SumTwo(make_console(), player, random.Random(5))
        assert [a.roll_dice() for _ in range(20)] == [b.roll_dice() for _ in range(20)]


class FixedRoll(SumTwo):
    """A SumTwo whose dice always come up as given."""

    def __init__(self, *args, rolls, **kwargs):
        super().__init__(*args, **kwargs)
        self._rolls = iter(rolls)

    def roll_dice(self):
        return next(self._rolls)


class TestPlay:
    def test_metadata(self):
        assert SumTwo.name == "SumTwo"
        assert SumTwo.is_gambling is True

    def test_winning_round_pays_out(self, player, make_console):
        console = make_console(["4", "10", "no"])  # Over 7, $10, stop
        FixedRoll(console, player, rolls=[9]).play()
        assert player.wallet.balance == D("520")
        assert "The roll was 9" in console.text
        assert "+20.00 dollars" in console.text

    def test_losing_round_costs_stake(self, player, make_console):
        console = make_console(["4", "10", "no"])
        FixedRoll(console, player, rolls=[3]).play()
        assert player.wallet.balance == D("490")
        assert "-10.00 dollars" in console.text

    def test_exactly_seven_pays_three_to_one(self, player, make_console):
        FixedRoll(make_console(["3", "100", "no"]), player, rolls=[7]).play()
        assert player.wallet.balance == D("800")

    def test_play_again_then_stop(self, player, make_console):
        console = make_console(["1", "10", "yes", "2", "10", "no"])
        FixedRoll(console, player, rolls=[4, 4]).play()  # even wins, odd loses
        assert player.wallet.balance == D("500")

    def test_quit_at_bet_menu(self, player, make_console):
        console = make_console(["quit"])
        SumTwo(console, player).play()
        assert player.wallet.balance == D("500")
        assert "Thanks for playing SumTwo!" in console.text

    def test_invalid_menu_choice_reprompts(self, player, make_console):
        console = make_console(["9", "abc", "quit"])
        SumTwo(console, player).play()
        assert console.text.count("Invalid choice") == 2

    @pytest.mark.parametrize("bad", ["abc", "", "0", "-5", "nan", "inf"])
    def test_invalid_amounts_reprompt(self, player, make_console, bad):
        console = make_console(["1", bad, "10", "no"])
        FixedRoll(console, player, rolls=[4]).play()
        assert "Invalid amount" in console.text
        assert player.wallet.balance == D("510")

    def test_cannot_bet_more_than_balance(self, player, make_console):
        console = make_console(["1", "500.01", "500", "no"])
        FixedRoll(console, player, rolls=[3]).play()
        assert "Insufficient funds" in console.text
        assert player.wallet.balance == D("0")

    def test_game_ends_when_player_is_broke(self, player, make_console):
        console = make_console(["1", "500"])  # no "roll again?" answer needed
        FixedRoll(console, player, rolls=[3]).play()
        assert "out of money" in console.text
        assert player.wallet.balance == D("0")

    def test_amount_rounded_to_cents(self, player, make_console):
        console = make_console(["1", "10.005", "no"])
        FixedRoll(console, player, rolls=[3]).play()  # even loses
        assert player.wallet.balance == D("489.99")
