
import os
from loader import load_user_intents, load_bids

def test_loader():
    intents = load_user_intents('./data/user_intents')
    bids = load_bids('./data/bids')
    assert len(intents) > 0, "No intents loaded"
    assert len(bids) > 0, "No bids loaded"
    print("✅ test_loader passed")

if __name__ == '__main__':
    test_loader()
