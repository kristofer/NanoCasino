from decimal import Decimal

from nanocasino.casino import Casino
from nanocasino.games import CoinFlip, Game, SumTwo, TwoCard


def run(answers, make_console, **kwargs):
    console = make_console(answers)
    casino = Casino(console, **kwargs)
    casino.run()
    return casino, console


def test_default_games(make_console):
    assert Casino(make_console()).games == [SumTwo, TwoCard, CoinFlip]


def test_exit_immediately(make_console):
    _, console = run(["5"], make_console)
    assert "Thank you for playing!" in console.text


def test_menu_lists_games_in_order(make_console):
    _, console = run(["5"], make_console)
    menu = console.output[0]
    assert "1. Register a player" in menu
    assert "2. Play SumTwo" in menu
    assert "3. Play TwoCardStud" in menu
    assert "4. Play CoinFlip" in menu
    assert "5. Exit" in menu


def test_register_player(make_console):
    casino, console = run(["1", "Kris", "5"], make_console)
    assert [p.name for p in casino.players] == ["Kris"]
    assert "Hello Kris" in console.text
    assert "You have $500.00" in console.text  # wallet shown on next menu


def test_choosing_a_game_registers_a_player_first(make_console):
    casino, console = run(["4", "Kris", "no", "5"], make_console)  # CoinFlip
    assert [p.name for p in casino.players] == ["Kris"]
    assert "Welcome to CoinFlip" in console.text


def test_player_reused_across_games(make_console):
    casino, _ = run(["4", "Kris", "no", "4", "no", "5"], make_console)
    assert len(casino.players) == 1


def test_wallet_changes_persist_between_games(make_console):
    casino, console = run(
        ["2", "Kris", "1", "100", "no", "5"], make_console
    )
    player = casino.players[0]
    assert f"You have {player.wallet}" in console.text
    assert player.wallet.balance in (Decimal("400"), Decimal("600"))


def test_invalid_choice(make_console):
    _, console = run(["9", "x", "", "5"], make_console)
    assert console.text.count("Invalid choice!") == 3


def test_eof_exits_cleanly(make_console):
    _, console = run([], make_console)
    assert "Thank you for playing!" in console.text


def test_custom_game_appears_in_menu_and_runs(make_console):
    class Roulette(Game):
        name = "Roulette"
        is_gambling = True
        played = False

        def play(self):
            Roulette.played = True
            self.console.tell("spin!")

    casino, console = run(["2", "Kris", "3"], make_console, games=[Roulette])
    assert "2. Play Roulette" in console.output[0]
    assert "3. Exit" in console.output[0]
    assert Roulette.played
    assert "spin!" in console.text


def test_add_game(make_console):
    casino = Casino(make_console(), games=[])
    casino.add_game(CoinFlip)
    assert casino.games == [CoinFlip]
