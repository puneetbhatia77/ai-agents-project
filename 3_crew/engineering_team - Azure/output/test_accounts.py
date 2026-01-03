import unittest
from accounts import Account, get_share_price

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('TraderJoe', 1000)

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)
        self.assertIn('Deposited: $500.00', self.account.list_transactions())

    def test_deposit_negative(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 800)
        self.assertIn('Withdrew: $200.00', self.account.list_transactions())

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(1500)

    def test_buy_shares(self):
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.balance, 1000 - 450)  # 3 * 150
        self.assertEqual(self.account.portfolio['AAPL'], 3)
        self.assertIn('Bought 3 shares of AAPL at $150.00 each.', self.account.list_transactions())

    def test_buy_shares_insufficient_funds(self):
        self.account.balance = 100
  
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 3)

    def test_sell_shares(self):
        self.account.buy_shares('AAPL', 3)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.balance, 1000 - 450 + 150)  # Recalculate
        self.assertEqual(self.account.portfolio['AAPL'], 2)
        self.assertIn('Sold 1 shares of AAPL at $150.00 each.', self.account.list_transactions())

    def test_sell_shares_not_enough(self):
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 1)

    def test_portfolio_value(self):
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.portfolio_value(), 1000 - 450)  # 3 shares

    def test_profit_loss(self):
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.profit_loss(), self.account.portfolio_value() - 1000)

    def test_report_holdings(self):
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.report_holdings(), {'AAPL': 3})

    def test_report_profit_loss(self):
        self.account.buy_shares('AAPL', 3)
        self.assertEqual(self.account.report_profit_loss(), self.account.profit_loss())

    def test_list_transactions(self):
        self.account.deposit(500)
        self.account.withdraw(200)
        self.assertEqual(len(self.account.list_transactions()), 2)

if __name__ == '__main__':
    unittest.main()