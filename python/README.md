# NanoCasino (Python)

A Python translation of the Java NanoCasino: three text-mode games (SumTwo
dice, TwoCardStud, CoinFlip), written to show idiomatic Python and a standard
project layout.

## Run it

```bash
cd python
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
nanocasino            # or: python -m nanocasino
pytest --cov=nanocasino
```

Requires Python 3.11+.

## Layout

```
python/
├── pyproject.toml          # metadata, dependencies, entry point, pytest config
├── src/nanocasino/         # "src layout": tests can only import the installed package
│   ├── __main__.py         # python -m nanocasino
│   ├── casino.py           # Casino: menu loop, player + game registration
│   ├── console.py          # Console protocol + TerminalConsole (all user I/O)
│   ├── cards.py            # Rank, Suit, Card, Deck, Hand
│   ├── player.py           # Player
│   ├── wallet.py           # Wallet, InsufficientFundsError
│   └── games/
│       ├── base.py         # Game (abstract base class)
│       ├── sum_two.py      # BetType, Bet, SumTwo
│       ├── two_card.py     # TwoCard
│       └── coin_flip.py    # CoinFlip
└── tests/                  # pytest; conftest.py has the scripted console fixture
```

## Java to Python: what changed and why

| Java | Python | Why |
|---|---|---|
| `PlayerInterface` + `SimplePlayer` | `Player` dataclass | Duck typing makes a one-implementation interface unnecessary. |
| `GameInterface` | `Game` ABC with `name` / `is_gambling` class attributes | An abstract base class is still right when subclasses must implement `play()`. |
| `SumItUp.BetType` enum + odds `HashMap` + `isBetWinner` if-chain | `BetType` enum whose members carry `label`, `odds` and a win predicate | Data and behaviour live together; no lookup tables to keep in sync. |
| `Card.Rank` enum + `cardValue()` switch | `Rank(IntEnum)` with a `points` property | `min(value, 10)` replaces a 13-arm switch. |
| `Card` with `final` fields, getters | `@dataclass(frozen=True, slots=True)` | Immutable, hashable, `__eq__` and `__repr__` for free. |
| `Hand.getAt/pop/size/showHand` | `__len__`, `__iter__`, `__str__`, `pop`, `total` | Hands behave like Python collections. |
| `Deck.size()`, `IllegalStateException` | `len(deck)`, `EmptyDeckError(IndexError)` | Protocols and exceptions Python programmers expect. |
| `double` money | `Decimal` | No floating-point cent errors. |
| `Wallet.withdraw` returns `boolean` | raises `InsufficientFundsError` | Errors are exceptions, not return codes. |
| `Casino` hard-codes `switch` menu | menu built from a list of game classes | Adding a game is one class and one list entry (the Java code asked "how would you add multiple games?"). |
| `Casino.promptUser/tellUser/wasteTime` | `Console` protocol; `TerminalConsole` | Dependency injection: tests pass a scripted console, no mocking library. |
| `Math.random()` / `new Random()` inside games | optional `random.Random` argument | Seeded, reproducible tests. |

## Behaviour fixes made during the translation

The Java code had a few bugs. The Python version fixes them rather than copying them:

- `SimplePlayer(String name)` did `name = name`, so `getName()` returned the default. Python `Player` stores the name.
- SumTwo looped forever on a bet of 0 or less, and on a broke player. Both are handled.
- TwoCard crashed when the deck ran out after 13 rounds. It now starts a fresh deck.
- `Deck` test expected `"HEARTS of KING"` while the code produced `"KING of HEARTS"`. Python prints `King of Hearts`.
- "Play again?" answers are consistent across games: only `y` / `yes` continues.
- Unimplemented `addPlayer` / `removePlayer` / `isGambling` stubs are gone; every game defines `name` and `is_gambling`.
- CoinFlip and TwoCard still involve no wagering, as in the original.
