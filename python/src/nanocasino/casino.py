"""The casino: registers players and games, and runs the main menu."""

from collections.abc import Iterable

from nanocasino.console import Console, TerminalConsole
from nanocasino.games import DEFAULT_GAMES, Game
from nanocasino.player import Player


class Casino:
    """The house. Owns the menu loop and hands games to players.

    >>> casino = Casino(games=[])
    >>> casino.games
    []
    """

    def __init__(
        self,
        console: Console | None = None,
        games: Iterable[type[Game]] = DEFAULT_GAMES,
    ) -> None:
        self.console = console or TerminalConsole()
        self.games: list[type[Game]] = list(games)
        self.players: list[Player] = []

    def add_game(self, game: type[Game]) -> None:
        self.games.append(game)

    def register_player(self, name: str | None = None) -> Player:
        """Add a player, asking for a name if one isn't given."""
        if name is None:
            name = self.console.prompt("What is your name? ").strip()
            self.console.tell(f"Hello {name}")
        player = Player(name)
        self.players.append(player)
        return player

    def run(self) -> None:
        """Main loop. This and the games are the only places that talk to the user."""
        player: Player | None = None
        try:
            while True:
                self._show_menu(player)
                choice = self.console.prompt("Enter your choice: ").strip()
                if choice == "1":
                    player = self.register_player()
                elif choice == str(len(self.games) + 2):
                    break
                elif choice.isdecimal() and 2 <= int(choice) <= len(self.games) + 1:
                    player = player or self.register_player()
                    game_class = self.games[int(choice) - 2]
                    game_class(self.console, player).play()
                else:
                    self.console.tell("Invalid choice!")
        except EOFError:
            pass  # input closed (Ctrl-D): leave quietly
        self.console.tell("Thank you for playing!")

    def _show_menu(self, player: Player | None) -> None:
        lines = ["Welcome to the BINARY casino!", "where every game is a power of Two!!"]
        if player:
            lines.append(f"***\nYou have {player.wallet}\n***\n")
        lines.append("1. Register a player")
        lines.extend(f"{n}. Play {game.name}" for n, game in enumerate(self.games, 2))
        lines.append(f"{len(self.games) + 2}. Exit")
        self.console.tell("\n".join(lines))
