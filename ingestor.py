from dto import UserIntentDTO, BidDTO
from graph_builder import GraphBuilder
from neo4j_driver import Neo4jClient

def ingest_pipeline(user_intent_json, bid_json):
    db = Neo4jClient("bolt://localhost:7687", "neo4j", "testtest")
    builder = GraphBuilder(db)

    print("Ingesting user intent and bids...", user_intent_json, bid_json)

    intent = UserIntentDTO(
        intentHash=user_intent_json["intentHash"],
        intentStatus=user_intent_json["intentStatus"],
        account=user_intent_json["account"],
        permittedAccounts=user_intent_json["userIntent"]["core"]["permittedAccounts"],
        desiredAssets=user_intent_json["userIntent"]["constraints"]["desiredAssets"],
        dispensableAssets=user_intent_json["userIntent"]["constraints"]["dispensableAssets"],
        slippage=user_intent_json["userIntent"]["constraints"]["slippagePercentage"],
        deadline=user_intent_json["userIntent"]["constraints"]["deadline"],
        createdAt=user_intent_json["createdAt"]
    )
    builder.insert_user_intent(intent)

    for b in bid_json:
        bid = BidDTO(
            bidHash=b["bidHash"],
            intentHash=b["intentHash"],
            solverAddress=b["solverAddress"],
            smartWalletAddress=b["smartWalletAddress"],
            status=b["bidStatus"],
            steps=b["bid"]["steps"],
            createdAt=b["createdAt"]
        )
        builder.insert_bid(bid)

    db.close()
