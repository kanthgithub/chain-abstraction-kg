
import logging
from loader import load_user_intents, load_bids
from neo4j_driver import Neo4jClient
from graph_builder import GraphBuilder

USER_INTENT_DIR = "./data/user_intents"
BID_DIR = "./data/bids"

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logging.info("🚀 Starting Chain Graph Pipeline")

    user_intents = load_user_intents(USER_INTENT_DIR)
    bids = load_bids(BID_DIR)

    db = Neo4jClient("bolt://localhost:7687", "neo4j", "testtest")
    builder = GraphBuilder(db)

    success_intents, failed_intents = 0, 0
    success_bids, failed_bids = 0, 0

    for intent in user_intents:
        try:
            builder.insert_user_intent(intent)
            success_intents += 1
        except Exception as e:
            logging.error(f"Failed to insert intent {intent.intentHash}: {e}")
            failed_intents += 1

    for bid in bids:
        try:
            builder.insert_bid(bid)
            success_bids += 1
        except Exception as e:
            logging.error(f"Failed to insert bid {bid.bidHash}: {e}")
            failed_bids += 1

    db.close()

    logging.info(f"""✅ Ingestion Summary:
    ✔️ UserIntents: {success_intents} inserted, {failed_intents} failed
    ✔️ Bids:        {success_bids} inserted, {failed_bids} failed
    """)

if __name__ == '__main__':
    main()
