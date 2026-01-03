import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account('1234', 'John Doe')

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 0.0)

    def test_deposit(self):
        self.account.deposit(100.0)
        self.assertEqual(self.account.balance, 100.0)
        self.assertIn('Deposited 100.0', self.account.get_transactions())

    def test_deposit_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-50.0)

    def test_withdraw(self):
        self.account.deposit(100.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.balance, 50.0)
        self.assertIn('Withdrew 50.0', self.account.get_transactions())

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(50.0)

    def test_buy_shares(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.holdings['AAPL'], 1)
        self.assertEqual(self.account.balance, 850.0)
        self.assertIn('Bought 1 shares of AAPL', self.account.get_transactions())

    def test_buy_shares_insufficient_funds(self):
        self.account.deposit(100.0)
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 1)

    def test_sell_shares(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 1)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.balance, 1000.0 + 150.0)
        self.assertIn('Sold 1 shares of AAPL', self.account.get_transactions())

    def test_sell_shares_insufficient_quantity(self):
        self.account.deposit(1000.0)
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 1)

    def test_get_portfolio_value(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.get_portfolio_value(), 1000.0 + 150.0)

    def test_get_profit_loss(self):
        self.account.deposit(1000.0)
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.get_profit_loss(), 150.0)

if __name__ == '__main__':
    unittest.main()