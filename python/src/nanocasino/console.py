"""All user I/O lives here.

Games and the casino talk to a :class:`Console`, never to ``print`` or
``input`` directly. That keeps them testable: tests hand in a scripted
console instead of patching builtins.
"""

import itertools
import sys
import time
from collections.abc import Callable
from typing import Protocol, TextIO

TWIRL_FRAMES = "/-\\|"
FRAME_SECONDS = 0.1


class Console(Protocol):
    """What a game needs from the outside world."""

    def tell(self, message: str) -> None:
        """Show a message to the user."""

    def prompt(self, message: str) -> str:
        """Show a message and return the user's reply."""

    def wait(self, seconds: float) -> None:
        """Pause (with a little animation) for dramatic effect."""


class TerminalConsole:
    """A :class:`Console` backed by text streams (stdin/stdout by default)."""

    def __init__(
        self,
        stdin: TextIO | None = None,
        stdout: TextIO | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._stdin = stdin or sys.stdin
        self._stdout = stdout or sys.stdout
        self._sleep = sleep

    def tell(self, message: str) -> None:
        print(message, file=self._stdout, flush=True)

    def prompt(self, message: str) -> str:
        self.tell(message)
        line = self._stdin.readline()
        if not line:
            raise EOFError("input stream closed")
        return line.rstrip("\r\n")

    def wait(self, seconds: float) -> None:
        frames = itertools.cycle(TWIRL_FRAMES)
        for _ in range(round(seconds / FRAME_SECONDS)):
            # "\r" returns the cursor to column 0 so frames overwrite each other.
            print(f"\r{next(frames)}", end="", file=self._stdout, flush=True)
            self._sleep(FRAME_SECONDS)
        print("\r ", file=self._stdout, flush=True)


def confirm(console: Console, question: str) -> bool:
    """Ask a yes/no question; anything but "y"/"yes" counts as no."""
    return console.prompt(question).strip().lower() in {"y", "yes"}
