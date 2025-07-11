from graph_builder import GraphBuilder
from neo4j_driver import Neo4jClient
from dto import UserIntentDTO, BidDTO

def ingest_pipeline(user_intent: UserIntentDTO, bids: list[BidDTO]):
    db = Neo4jClient("bolt://localhost:7687", "neo4j", "testtest")
    builder = GraphBuilder(db)

    print("Ingesting user intent and bids...", user_intent, bids)
    builder.insert_user_intent(user_intent)

    for bid in bids:
        builder.insert_bid(bid)

    db.close()