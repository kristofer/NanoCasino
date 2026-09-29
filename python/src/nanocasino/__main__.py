"""Entry point: ``python -m nanocasino`` or the ``nanocasino`` script."""

from nanocasino.casino import Casino


def main() -> None:
    Casino().run()


if __name__ == "__main__":
    main()
