import random

import pytest

from nanocasino.games.coin_flip import SUSPENSE_SECONDS, CoinFlip


class FixedFlips(CoinFlip):
    def __init__(self, *args, flips, **kwargs):
        super().__init__(*args, **kwargs)
        self._flips = iter(flips)

    def flip(self):
        return next(self._flips)


def test_metadata():
    assert CoinFlip.name == "CoinFlip"
    assert CoinFlip.is_gambling is False


def test_flip_is_fair(player, make_console):
    game = CoinFlip(make_console(), player, random.Random(42))
    n = 100_000
    heads = sum(game.flip() for _ in range(n))
    assert abs(heads - (n - heads)) < n / 100 * 2


def test_seeded_flips_are_reproducible(player, make_console):
    a = CoinFlip(make_console(), player, random.Random(8))
    b = CoinFlip(make_console(), player, random.Random(8))
    assert [a.flip() for _ in range(50)] == [b.flip() for _ in range(50)]


def test_heads_wins(player, make_console):
    console = make_console(["no"])
    FixedFlips(console, player, flips=[True]).play()
    assert "HEADS" in console.text
    assert "You win!" in console.text


def test_tails_loses(player, make_console):
    console = make_console(["no"])
    FixedFlips(console, player, flips=[False]).play()
    assert "TAILS" in console.text
    assert "The dealer wins!" in console.text


def test_plays_again_until_declined(player, make_console):
    console = make_console(["yes", "YES", "no"])
    FixedFlips(console, player, flips=[True, False, True]).play()
    assert console.text.count("Flipping the coin...") == 3
    assert console.waits == [SUSPENSE_SECONDS] * 3


@pytest.mark.parametrize("answer", ["", "maybe", "n"])
def test_anything_but_yes_ends_game(player, make_console, answer):
    console = make_console([answer])
    FixedFlips(console, player, flips=[True]).play()
    assert console.text.count("Flipping the coin...") == 1


def test_no_money_changes_hands(player, make_console):
    before = player.wallet.balance
    FixedFlips(make_console(["no"]), player, flips=[False]).play()
    assert player.wallet.balance == before
