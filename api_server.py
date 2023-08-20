from fastapi import FastAPI, HTTPException
from .db_handler import get_transaction_by_hash, get_aggregate_stats
from .transaction import Transaction
from pydantic import BaseModel
from process_transactions import transactions_data

app = FastAPI()

class TransactionResponse(BaseModel):
    hash: str
    fromAddress: str
    toAddress: str
    blockNumber: int
    executedAt: str
    gasUsed: int
    gasCostInDollars: float

class StatsResponse(BaseModel):
    totalTransactionsInDB: int
    totalGasUsed: int
    totalGasCostInDollars: int

@app.get("/transactions/{transaction_hash}", response_model=TransactionResponse)
async def get_transaction(transaction_hash: str):
    transaction = get_transaction_by_hash(transaction_hash)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {
        "hash": transaction.hash,
        "fromAddress": transaction.from_address,
        "toAddress": transaction.to_address,
        "blockNumber": transaction.block_number,
        "executedAt": transaction.execution_timestamp.strftime("%b-%d-%Y %I:%M:%S %p +UTC"),
        "gasUsed": transaction.gas,
        "gasCostInDollars": transaction.gas_cost_dollars
        # You need to ensure this attribute is populated in your Transaction instances.
    }

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    stats = get_aggregate_stats()
    return stats
