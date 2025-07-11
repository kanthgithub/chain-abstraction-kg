from loader import load_user_intents, load_bids
from ingestor import ingest_pipeline

user_intents = load_user_intents("data/user_intents")
bids = load_bids("data/bids")

for user_intent in user_intents:
    # Filter bids for this intent
    related_bids = [b for b in bids if b.intentHash == user_intent.intentHash]
    ingest_pipeline(user_intent, related_bids)