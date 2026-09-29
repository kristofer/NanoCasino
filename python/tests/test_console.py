import io

import pytest

from nanocasino.console import TerminalConsole, confirm


def make(text=""):
    out, sleeps = io.StringIO(), []
    console = TerminalConsole(io.StringIO(text), out, sleeps.append)
    return console, out, sleeps


def test_tell_writes_line():
    console, out, _ = make()
    console.tell("hi")
    assert out.getvalue() == "hi\n"


def test_prompt_shows_message_and_returns_stripped_line():
    console, out, _ = make("Kris\r\nnext\n")
    assert console.prompt("Name?") == "Kris"
    assert console.prompt("Again?") == "next"
    assert "Name?" in out.getvalue()


def test_prompt_raises_eof_when_input_closed():
    console, _, _ = make("")
    with pytest.raises(EOFError):
        console.prompt("?")


def test_wait_animates_and_sleeps_for_requested_time():
    console, out, sleeps = make()
    console.wait(1)
    assert sum(sleeps) == pytest.approx(1)
    assert {"/", "-", "\\", "|"} <= set(out.getvalue())
    assert out.getvalue().endswith("\r \n")


@pytest.mark.parametrize(
    ("answer", "expected"),
    [("yes", True), ("Y", True), (" YES ", True),
     ("no", False), ("", False), ("yep", False)],
)
def test_confirm(answer, expected, make_console):
    assert confirm(make_console([answer]), "ok?") is expected
