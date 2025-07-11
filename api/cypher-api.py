from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from neo4j_driver import Neo4jClient
from query import bid_queries

app = FastAPI(title="Bid Query API")

def get_db():
    db = Neo4jClient("bolt://localhost:7687", "neo4j", "testtest")
    try:
        yield db
    finally:
        db.close()

# POSTMAN: GET http://localhost:8000/bids/by-solver?solver_address=0xABC...
@app.get("/bids/by-solver")
def bids_by_solver(
    solver_address: str = Query(..., description="Solver address"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        print(f"Fetching bids for solver: {solver_address}")
        bids = bid_queries.get_bids_by_solver(solver_address, db)
        return bids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POSTMAN: GET http://localhost:8000/bids/by-intent?intent_hash=0xABC...
@app.get("/bids/by-intent")
def bids_by_intent(
    intent_hash: str = Query(..., description="UserIntent hash"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        bids = bid_queries.get_bids_for_intent(intent_hash, db)
        return bids
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POSTMAN: GET http://localhost:8000/bids/steps-tokens?bid_hash=0xABC...
@app.get("/bids/steps-tokens")
def steps_and_tokens(
    bid_hash: str = Query(..., description="Bid hash"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_steps_and_tokens_for_bid(bid_hash, db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POSTMAN: GET http://localhost:8000/bids/by-account?account_address=0xABC...
@app.get("/bids/by-account")
def bids_by_account(
    account_address: str = Query(..., description="Account address"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_bids_for_account(account_address, db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# POSTMAN: GET http://localhost:8000/solvers/by-account?account_address=0xABC...
@app.get("/solvers/by-account")
def solvers_by_account(
    account_address: str = Query(..., description="Account address"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_solvers_for_account(account_address, db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Get the full bid path: Account → UserIntent → Bid → Solver
# POSTMAN: GET http://localhost:8000/bids/paths
@app.get("/bids/paths")
def bid_paths(db: Neo4jClient = Depends(get_db)):
    try:
        return bid_queries.get_bid_paths(db)
    except RuntimeError as e:
        # Handle known errors from run_query
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail="Unexpected server error")
    
# 7. Get all tokens transferred in all steps for a given solver (crazy traversal)
# POSTMAN: GET http://localhost:8000/bids/tokens-by-solver?solver_address=0xABC...
@app.get("/bids/tokens-by-solver")
def tokens_by_solver(
    solver_address: str = Query(..., description="Solver address"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_all_tokens_transferred_by_solver(solver_address, db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 8. Find the most active solver (mind-blowing analytics)
# POSTMAN: GET http://localhost:8000/solvers/most-active
@app.get("/solvers/most-active")
def most_active_solver(
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_most_active_solver(db)
        if not data:
            raise HTTPException(status_code=404, detail="No solvers found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. Find all accounts whose intents have never received a bid (deep negative traversal)
# POSTMAN: GET http://localhost:8000/accounts/no-bids
@app.get("/accounts/no-bids")
def accounts_with_no_bids(
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_accounts_with_no_bids(db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 10. Get the full execution trace for a bid (if you add executions)
# POSTMAN: GET http://localhost:8000/bids/execution-trace?bid_hash=0xABC...
@app.get("/bids/execution-trace")
def execution_trace(
    bid_hash: str = Query(..., description="Bid hash"),
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_execution_trace_for_bid(bid_hash, db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))