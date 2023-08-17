Link to Rated Coding Challenge: https://github.com/rated-network/coding-challenge  
My steps:  
1. Parse CSV and extract relevant fields into objects representing each transaction. Calculate execution timestamp by adding block timestamp and assuming 12-second block time.  
2. Calculate gas cost in Gwei by multiplying gasUsed and gasPrice for each transaction.  
3. Use Coingecko API to get ETH price at execution time. Multiply gas cost in Gwei by ETH price to get gas cost in dollars.  
4. Save processed transactions to a local SQLite database.  
5. Build a FastAPI server with two endpoints:
- GET /transactions/:hash - Returns a single transaction details
- GET /stats - Returns aggregate stats about all transactions