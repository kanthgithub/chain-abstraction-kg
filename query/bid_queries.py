from neo4j_driver import Neo4jClient
import logging
logger = logging.getLogger("bid_queries")
logger.setLevel(logging.INFO)

# 1. Get all bids responded by a given solver
def get_bids_by_solver(solver_address: str, db: Neo4jClient):
    try:
        logger.info(f"DB Query -> Fetching bids for solver: {solver_address}")
        query = """
        MATCH (s:Solver {address: $solverAddress})-[:RESPONDED_WITH]->(b:Bid)
        RETURN b
        """
        result = db.run_query(query, {"solverAddress": solver_address})
        records = list(result)  # <-- Convert to list immediately!
        #logger.info(f"DB Query -> Found {result} bids for solver: {solver_address}")
        return [record["b"] for record in records]
    except Exception as e:
        logger.error(f"Error fetching bids for solver {solver_address}: {e}")
        raise RuntimeError(f"Failed to fetch bids for solver {solver_address}: {e}")


# 2. Get all bids for a given user intent
def get_bids_for_intent(intent_hash: str, db: Neo4jClient):
    query = """
    MATCH (b:Bid)-[:BID_FOR]->(i:UserIntent {intentHash: $intentHash})
    RETURN b
    """
    result = db.run_query(query, {"intentHash": intent_hash})
    return [record["b"] for record in result]

# 3. Get all steps and tokens for a given bid
def get_steps_and_tokens_for_bid(bid_hash: str, db: Neo4jClient):
    query = """
    MATCH (b:Bid {bidHash: $bidHash})-[:TRANSFER_STEP]->(t:Token)
    RETURN t, b
    """
    result = db.run_query(query, {"bidHash": bid_hash})
    return [{"token": record["t"], "bid": record["b"]} for record in result]

# 4. Get all bids for a user (by account address)
def get_bids_for_account(account_address: str, db: Neo4jClient):
    query = """
    MATCH (a:Account {address: $account})-[:PLACED]->(i:UserIntent)<-[:BID_FOR]-(b:Bid)
    RETURN b, i
    """
    result = db.run_query(query, {"account": account_address})
    return [{"bid": record["b"], "intent": record["i"]} for record in result]

# 5. Get all solvers who have ever responded to a user's intents
def get_solvers_for_account(account_address: str, db: Neo4jClient):
    query = """
    MATCH (a:Account {address: $account})-[:PLACED]->(i:UserIntent)<-[:BID_FOR]-(b:Bid)<-[:RESPONDED_WITH]-(s:Solver)
    RETURN DISTINCT s
    """
    result = db.run_query(query, {"account": account_address})
    return [record["s"] for record in result]

# 6. Get the full bid path: Account → UserIntent → Bid → Solver
def get_bid_paths(db: Neo4jClient):
    query = """
    MATCH (a:Account)-[:PLACED]->(i:UserIntent)<-[:BID_FOR]-(b:Bid)<-[:RESPONDED_WITH]-(s:Solver)
    RETURN a, i, b, s
    """
    result = db.run_query(query)
    records = list(result)  # Convert to list IMMEDIATELY
    return [{"account": r["a"], "intent": r["i"], "bid": r["b"], "solver": r["s"]} for r in records]

# 7. Get all tokens transferred in all steps for a given solver (crazy traversal)
def get_all_tokens_transferred_by_solver(solver_address: str, db: Neo4jClient):
    query = """
    MATCH (s:Solver {address: $solverAddress})-[:RESPONDED_WITH]->(b:Bid)-[ts:TRANSFER_STEP]->(t:Token)
    RETURN b.bidHash AS bidHash, ts.sequence AS stepSeq, t.address AS tokenAddress, ts.amount AS amount, ts.action AS action
    ORDER BY bidHash, stepSeq
    """
    result = db.run_query(query, {"solverAddress": solver_address})
    return [dict(record) for record in result]

# 8. Find the most active solver (mind-blowing analytics)
def get_most_active_solver(db: Neo4jClient):
    query = """
    MATCH (s:Solver)-[:RESPONDED_WITH]->(b:Bid)
    RETURN s.address AS solver, count(b) AS bidCount
    ORDER BY bidCount DESC
    LIMIT 1
    """
    result = db.run_query(query)
    return result.single()

# 9. Find all accounts whose intents have never received a bid (deep negative traversal)
def get_accounts_with_no_bids(db: Neo4jClient):
    query = """
    MATCH (a:Account)-[:PLACED]->(i:UserIntent)
    WHERE NOT (i)<-[:BID_FOR]-(:Bid)
    RETURN a, i
    """
    result = db.run_query(query)
    return [{"account": r["a"], "intent": r["i"]} for r in result]

# 10. Get the full execution trace for a bid (if you add executions)
def get_execution_trace_for_bid(bid_hash: str, db: Neo4jClient):
    query = """
    MATCH (b:Bid {bidHash: $bidHash})-[:TRANSFER_STEP]->(t:Token)
    OPTIONAL MATCH (b)-[:HAS_STEP]->(step)-[:HAS_EXECUTION]->(e:Execution)
    RETURN b, t, step, e
    """
    result = db.run_query(query, {"bidHash": bid_hash})
    return [dict(record) for record in result]
