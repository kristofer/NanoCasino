from decimal import Decimal

import pytest

from nanocasino.player import STARTING_BALANCE, Player
from nanocasino.wallet import InsufficientFundsError, Wallet


class TestWallet:
    def test_deposit_and_withdraw(self):
        wallet = Wallet("a", Decimal("100"))
        wallet.deposit(Decimal("25.50"))
        wallet.withdraw(Decimal("10"))
        assert wallet.balance == Decimal("115.50")

    def test_withdraw_more_than_balance_raises_and_leaves_balance(self):
        wallet = Wallet("a", Decimal("10"))
        with pytest.raises(InsufficientFundsError):
            wallet.withdraw(Decimal("10.01"))
        assert wallet.balance == Decimal("10")

    def test_withdraw_entire_balance(self):
        wallet = Wallet("a", Decimal("10"))
        wallet.withdraw(Decimal("10"))
        assert wallet.balance == 0

    @pytest.mark.parametrize("amount", [Decimal("0"), Decimal("-5")])
    def test_non_positive_amounts_rejected(self, amount):
        wallet = Wallet("a")
        with pytest.raises(ValueError):
            wallet.deposit(amount)
        with pytest.raises(ValueError):
            wallet.withdraw(amount)

    def test_can_afford(self):
        wallet = Wallet("a", Decimal("50"))
        assert wallet.can_afford(Decimal("50"))
        assert not wallet.can_afford(Decimal("50.01"))

    def test_str_is_dollars_and_cents(self):
        assert str(Wallet("a", Decimal("1234.5"))) == "$1,234.50"

    def test_balance_coerced_to_decimal(self):
        assert isinstance(Wallet("a", 5).balance, Decimal)

    def test_decimal_arithmetic_is_exact(self):
        wallet = Wallet("a", Decimal("0"))
        for _ in range(10):
            wallet.deposit(Decimal("0.10"))
        assert wallet.balance == Decimal("1.00")


class TestPlayer:
    def test_new_player_gets_starting_balance(self):
        player = Player("Kris")
        assert player.name == "Kris"
        assert player.wallet.balance == STARTING_BALANCE
        assert player.wallet.account_id == "Kris"

    def test_players_do_not_share_wallets(self):
        a, b = Player("a"), Player("b")
        a.wallet.withdraw(Decimal("100"))
        assert b.wallet.balance == STARTING_BALANCE
