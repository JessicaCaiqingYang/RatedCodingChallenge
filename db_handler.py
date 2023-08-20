import sqlite3
from .transaction import Transaction

# Path to your SQLite database. Change this to your actual path.
DB_PATH = 'transactions.db'


def create_connection():
    """Establish a connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        print(e)
    return conn


def get_transaction_by_hash(transaction_hash: str) -> Transaction:
    """Retrieve a transaction by its hash."""

    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE hash=?", (transaction_hash,))

        row = cur.fetchone()
        if row:
            # Assuming the columns in your transactions table match the Transaction class attributes
            return Transaction(
                hash=row[0],
                nonce=row[1],
                block_hash=row[2],
                block_number=row[3],
                transaction_index=row[4],
                from_address=row[5],
                to_address=row[6],
                value=row[7],
                gas=row[8],
                gas_price=row[9],
                block_timestamp=row[10]
            )
    return None


def get_aggregate_stats():
    """Retrieve aggregated stats about transactions."""

    conn = create_connection()
    with conn:
        cur = conn.cursor()

        # Fetching total number of transactions
        cur.execute("SELECT COUNT(*) FROM transactions")
        total_transactions = cur.fetchone()[0]

        # Fetching total gas used
        cur.execute("SELECT SUM(gas) FROM transactions")
        total_gas = cur.fetchone()[0]

        # Assuming you have a 'gas_cost_dollars' column in your transactions table.
        cur.execute("SELECT SUM(gas_cost_dollars) FROM transactions")
        total_gas_cost = cur.fetchone()[0]

    return {
        'totalTransactionsInDB': total_transactions,
        'totalGasUsed': total_gas,
        'totalGasCostInDollars': total_gas_cost
    }
