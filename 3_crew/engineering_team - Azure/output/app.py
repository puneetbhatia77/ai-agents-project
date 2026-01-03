from accounts import Account
import gradio as gr

# Create an instance of Account for demonstration
account = Account(account_id="1", owner_name="Demo User")

def create_account():
    return "Account created!"

def deposit_funds(amount):
    try:
        account.deposit(amount)
        return f"Deposited {amount}. New Balance: {account.balance}"
    except ValueError as e:
        return str(e)

def withdraw_funds(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew {amount}. New Balance: {account.balance}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. New Holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. New Holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def show_portfolio_value():
    return f"Total Portfolio Value: {account.get_portfolio_value()}"

def show_profit_loss():
    return f"Profit/Loss: {account.get_profit_loss()}"

def show_holdings():
    return f"Current Holdings: {account.get_holdings()}"

def show_transactions():
    return f"Transactions: {account.get_transactions()}"

with gr.Blocks() as demo:
    gr.Markdown("## Trading Account Management System")
    
    gr.Button("Create Account").click(create_account)
    
    with gr.Row():
        amount_input = gr.Number(label="Amount")
        gr.Button("Deposit").click(deposit_funds, inputs=amount_input, outputs="output")
        gr.Button("Withdraw").click(withdraw_funds, inputs=amount_input, outputs="output")

    with gr.Row():
        symbol_input = gr.Textbox(label="Symbol (e.g., AAPL, TSLA)")
        quantity_input = gr.Number(label="Quantity")
        gr.Button("Buy Shares").click(buy_shares, inputs=[symbol_input, quantity_input], outputs="output")
        gr.Button("Sell Shares").click(sell_shares, inputs=[symbol_input, quantity_input], outputs="output")

    gr.Button("Show Portfolio Value").click(show_portfolio_value, outputs="output")
    gr.Button("Show Profit/Loss").click(show_profit_loss, outputs="output")
    gr.Button("Show Holdings").click(show_holdings, outputs="output")
    gr.Button("Show Transactions").click(show_transactions, outputs="output")
    
    output = gr.Textbox(label="Status", readonly=True)

demo.launch()