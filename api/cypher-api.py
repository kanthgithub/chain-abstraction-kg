from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from neo4j_driver import Neo4jClient
from query import bid_queries

app = FastAPI(title="Bid Query API")

# global variable for the Neo4j client
neo4j_client: Optional[Neo4jClient] = None

@app.on_event("startup")
def startup_event():
    global neo4j_client
    neo4j_client = Neo4jClient("bolt://localhost:7687", "neo4j", "testtest")

@app.on_event("shutdown")
def shutdown_event():
    global neo4j_client
    if neo4j_client:
        neo4j_client.close()

def get_db():
    # Dependency that returns the singleton client
    return neo4j_client

# Returns all bids responded by a given solver address.
# Query Parameters:
#   - solver_address: str (required) - The address of the solver.
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

# Returns all bids for a given user intent.
# Query Parameters:
#   - intent_hash: str (required) - The hash of the user intent.
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

# Returns all steps and tokens for a given bid.
# Query Parameters:
#   - bid_hash: str (required) - The hash of the bid.
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


# Returns all bids for a given account address.
# Query Parameters:
#   - account_address: str (required) - The address of the account.
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

# Returns all solvers who have ever responded to a user's intents.
# Query Parameters:
#   - account_address: str (required) - The address of the account.
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

# Returns the full bid path: Account → UserIntent → Bid → Solver.
# No query parameters.
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
    
# Get all tokens transferred in all steps for a given solver (crazy traversal)
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


# Find the most active solver (mind-blowing analytics)
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

# Find all accounts whose intents have never received a bid (deep negative traversal)
@app.get("/accounts/no-bids")
def accounts_with_no_bids(
    db: Neo4jClient = Depends(get_db)
):
    try:
        data = bid_queries.get_accounts_with_no_bids(db)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get the full execution trace for a bid (if you add executions)
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