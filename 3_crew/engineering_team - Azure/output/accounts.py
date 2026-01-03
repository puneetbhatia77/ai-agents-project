# accounts.py

class Account:
    def __init__(self, account_id: str, owner_name: str):
        self.account_id = account_id
        self.owner_name = owner_name
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = 0.0
        
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError('Deposit amount must be greater than zero.')
        if self.initial_deposit == 0:
            self.initial_deposit = amount
        self.balance += amount
        self.transactions.append(f'Deposited {amount}')

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError('Insufficient funds for withdrawal.')
        self.balance -= amount
        self.transactions.append(f'Withdrew {amount}')

    def buy_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be greater than zero.')
        total_cost = get_share_price(symbol) * quantity
        if total_cost > self.balance:
            raise ValueError('Not enough funds to buy shares.')
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append(f'Bought {quantity} shares of {symbol}')

    def sell_shares(self, symbol: str, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError('Quantity must be greater than zero.')
        if self.holdings.get(symbol, 0) < quantity:
            raise ValueError('Not enough shares to sell.')
        total_sale = get_share_price(symbol) * quantity
        self.balance += total_sale
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append(f'Sold {quantity} shares of {symbol}')

    def get_portfolio_value(self) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transactions(self) -> list:
        return self.transactions

    def __str__(self) -> str:
        holdings_str = ', '.join([f'{sym}: {qty}' for sym, qty in self.holdings.items()])
        return f'Account ID: {self.account_id}, Owner: {self.owner_name}, Balance: {self.balance}, Holdings: {holdings_str}'

# Test implementation of get_share_price
def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.00,
        'TSLA': 700.00,
        'GOOGL': 2800.00
    }
    return prices.get(symbol, 0.0)