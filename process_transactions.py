import requests
from .transaction import process_transactions_from_csv


def process_transactions():
    GWEI_TO_ETH = 1e-9
    transactions = process_transactions_from_csv('transactions.csv')

    # Loop through transactions
    for transaction in transactions:
        # Get ETH price in dollars at execution timestamp
        eth_price_url = f"https://api.coingecko.com/api/v3/coins/ethereum/history?from_timestamp={int(transaction.execution_timestamp.timestamp())}"
        eth_price_resp = requests.get(eth_price_url)
        eth_price = eth_price_resp.json()['market_data']['current_price']['usd']
        # Calculate gas cost in dollars
        gas_cost_dollars = transaction.gas * transaction.gas_price * GWEI_TO_ETH * eth_price
        # Add gas cost to transaction
        transaction.gas_cost_dollars = gas_cost_dollars
    return transactions

transactions_data = process_transactions()