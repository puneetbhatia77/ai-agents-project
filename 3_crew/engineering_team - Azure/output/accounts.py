# accounts.py

class Account:
    """
    A class to represent a user's trading account.
    """

    def __init__(self, username: str, initial_deposit: float):
        """
        Initializes an account with a username and an initial deposit.
        :param username: The name of the user.
        :param initial_deposit: The initial amount of money to deposit in the account.
        """
        self.username = username
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit  # Store initial deposit
        self.portfolio = {}
        self.transactions = []

    def deposit(self, amount: float):
        """
        Deposits funds into the account.
        :param amount: The amount to deposit.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(f"Deposited: ${amount:.2f}")

    def withdraw(self, amount: float):
        """
        Withdraws funds from the account if sufficient balance is available.
        :param amount: The amount to withdraw.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(f"Withdrew: ${amount:.2f}")

    def buy_shares(self, symbol: str, quantity: int):
        """
        Buys a specified quantity of shares of a stock.
        :param symbol: The stock symbol to buy shares of.
        :param quantity: The number of shares to buy.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity

        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")

        self.balance -= total_cost
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
        self.transactions.append(f"Bought {quantity} shares of {symbol} at ${share_price:.2f} each.")

    def sell_shares(self, symbol: str, quantity: int):
        """
        Sells a specified quantity of shares of a stock.
        :param symbol: The stock symbol to sell shares of.
        :param quantity: The number of shares to sell.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError("Not enough shares to sell.")

        share_price = get_share_price(symbol)
        total_earning = share_price * quantity

        self.balance += total_earning
        self.portfolio[symbol] -= quantity

        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]  # Remove stock if no shares left
        
        self.transactions.append(f"Sold {quantity} shares of {symbol} at ${share_price:.2f} each.")

    def portfolio_value(self) -> float:
        """
        Calculates the total current value of the user's portfolio.
        :return: The total value of all holdings.
        """
        total_value = self.balance
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        :return: The profit or loss.
        """
        return self.portfolio_value() - self.initial_deposit

    def report_holdings(self) -> dict:
        """
        Reports the current stock holdings of the user.
        :return: A dictionary of holdings.
        """
        return self.portfolio

    def report_profit_loss(self) -> float:
        """
        Reports the current profit or loss of the user.
        :return: The current profit or loss.
        """
        return self.profit_loss()

    def list_transactions(self) -> list:
        """
        Lists all transactions made by the user.
        :return: A list of transaction records.
        """
        return self.transactions

def get_share_price(symbol: str) -> float:
    """
    Returns the current price for a given stock symbol.
    This is a mock implementation that provides fixed prices for testing.
    :param symbol: Stock symbol.
    :return: The current price of the stock.
    """
    prices = {
        "AAPL": 150.00,
        "TSLA": 700.00,
        "GOOGL": 2800.00,
    }
    return prices.get(symbol, 0.0)

# Example usage (can be commented out): 
if __name__ == "__main__":
    account = Account("TraderJoe", 1000)
    account.deposit(500)
    account.buy_shares("AAPL", 3)
    account.sell_shares("AAPL", 1)
    print("Portfolio Value:", account.portfolio_value())
    print("Current Holdings:", account.report_holdings())
    print("Profit/Loss:", account.report_profit_loss())
    print("Transactions:", account.list_transactions())