import gradio as gr
from accounts import Account

# Create account instance at module level
account = Account("TraderJoe", 1000)

def create_account(initial_deposit):
    global account
    account = Account("TraderJoe", initial_deposit)
    return f"Account created with initial deposit of ${initial_deposit:.2f}"

def deposit(amount):
    try:
        account.deposit(amount)
        return f"Deposited: ${amount:.2f}. Current Balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def withdraw(amount):
    try:
        account.withdraw(amount)
        return f"Withdrew: ${amount:.2f}. Current Balance: ${account.balance:.2f}"
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    try:
        account.buy_shares(symbol, quantity)
        return f"Bought {quantity} shares of {symbol}. Current Holdings: {account.report_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    try:
        account.sell_shares(symbol, quantity)
        return f"Sold {quantity} shares of {symbol}. Current Holdings: {account.report_holdings()}"
    except ValueError as e:
        return str(e)

def portfolio_value():
    return f"Portfolio Value: ${account.portfolio_value():.2f}"

def profit_loss():
    return f"Profit/Loss: ${account.profit_loss():.2f}"

def list_transactions():
    transactions = account.list_transactions()
    return "\n".join(transactions) if transactions else "No transactions found."

with gr.Blocks() as app:
    gr.Markdown("### Trading Account Management System")
    
    with gr.Tab("Account Operations"):
        initial_deposit = gr.Number(label="Initial Deposit", value=1000)
        create_button = gr.Button("Create Account")
        create_output = gr.Textbox(label="Output", interactive=False)
        create_button.click(create_account, inputs=initial_deposit, outputs=create_output)
        
        deposit_amount = gr.Number(label="Deposit Amount")
        deposit_button = gr.Button("Deposit Funds")
        deposit_output = gr.Textbox(label="Output", interactive=False)
        deposit_button.click(deposit, inputs=deposit_amount, outputs=deposit_output)
        
        withdraw_amount = gr.Number(label="Withdrawal Amount")
        withdraw_button = gr.Button("Withdraw Funds")
        withdraw_output = gr.Textbox(label="Output", interactive=False)
        withdraw_button.click(withdraw, inputs=withdraw_amount, outputs=withdraw_output)

    with gr.Tab("Shares Operations"):
        buy_symbol = gr.Textbox(label="Stock Symbol (AAPL, TSLA, GOOGL)")
        buy_quantity = gr.Number(label="Quantity")
        buy_button = gr.Button("Buy Shares")
        buy_output = gr.Textbox(label="Output", interactive=False)
        buy_button.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
        
        sell_symbol = gr.Textbox(label="Stock Symbol")
        sell_quantity = gr.Number(label="Quantity")
        sell_button = gr.Button("Sell Shares")
        sell_output = gr.Textbox(label="Output", interactive=False)
        sell_button.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)

    with gr.Tab("Portfolio Summary"):
        value_button = gr.Button("Get Portfolio Value")
        value_output = gr.Textbox(label="Output", interactive=False)
        value_button.click(portfolio_value, outputs=value_output)
        
        profit_loss_button = gr.Button("Get Profit/Loss")
        profit_loss_output = gr.Textbox(label="Output", interactive=False)
        profit_loss_button.click(profit_loss, outputs=profit_loss_output)

    with gr.Tab("Transaction History"):
        transactions_button = gr.Button("List Transactions")
        transactions_output = gr.Textbox(label="Output", interactive=False)
        transactions_button.click(list_transactions, outputs=transactions_output)

if __name__ == "__main__":
    app.launch()