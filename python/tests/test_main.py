from unittest.mock import patch

from nanocasino.__main__ import main


def test_main_runs_a_casino():
    with patch("nanocasino.__main__.Casino") as casino_class:
        main()
    casino_class.return_value.run.assert_called_once_with()
