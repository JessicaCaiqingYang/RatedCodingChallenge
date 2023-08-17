from dataclasses import dataclass
from datetime import datetime, timedelta

# Store genesis block time as a constant
GENESIS_BLOCK_TIME = datetime.strptime("Jul-30-2015 03:26:28 PM +UTC", "%b-%d-%Y %I:%M:%S %p +UTC")


# Dataclass to represent a single Ethereum transaction
@dataclass
class Transaction:

    # Transaction hash
    hash: str
    
    # Transaction nonce
    nonce: int  

    # Hash of the block this transaction is in
    block_hash: str

    # Block number of the block this transaction is in
    block_number: int  

    # Index of the transaction within the block 
    transaction_index: int

    # Address of the sender
    from_address: str

    # Address of the receiver  
    to_address: str

    # Amount transferred (in wei)
    value: int  

    # Gas used for this transaction 
    gas: int

    # Gas price set by the sender (in wei)
    gas_price: int

    # Timestamp of the block this transaction is in 
    block_timestamp: datetime

    # Calculate transaction execution timestamp by using 12 seconds to approximate each block duration
    @property
    def execution_timestamp(self):
        return GENESIS_BLOCK_TIME + timedelta(seconds=self.block_number * 12)



# Open transactions CSV file 
import csv

with open('transactions.csv') as f:
    reader = csv.DictReader(f)

    transactions = []
    for row in reader:
        # Pass in only relevant fields to Transaction
        transaction = Transaction(
            hash=row['hash'],
            nonce=int(row['nonce']),
            block_hash=row['block_hash'],
            block_number=int(row['block_number']),
            transaction_index=int(row['transaction_index']),
            from_address=row['from_address'],
            to_address=row['to_address'],
            value=int(row['value']),
            gas=int(row['gas']),
            gas_price=int(row['gas_price']),
            block_timestamp=datetime.strptime(row['block_timestamp'], '%Y-%m-%d %H:%M:%S.%f %Z')
        )
        transactions.append(transaction)


import requests

GWEI_TO_ETH = 1e-9
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