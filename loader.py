
import os
import json
import logging
from dto import UserIntentDTO, BidDTO
from typing import List

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_user_intents(directory: str) -> List[UserIntentDTO]:
    intents = []
    for file in os.listdir(directory):
        if not file.startswith("user_intent_") or not file.endswith(".json"):
            continue
        path = os.path.join(directory, file)
        try:
            with open(path, 'r') as f:
                raw = json.load(f)
                dto = UserIntentDTO(
                    intentHash=raw["intentHash"],
                    intentStatus=raw["intentStatus"],
                    account=raw["account"],
                    permittedAccounts=raw["userIntent"]["core"]["permittedAccounts"],
                    desiredAssets=raw["userIntent"]["constraints"]["desiredAssets"],
                    dispensableAssets=raw["userIntent"]["constraints"]["dispensableAssets"],
                    slippage=raw["userIntent"]["constraints"]["slippagePercentage"],
                    deadline=raw["userIntent"]["constraints"]["deadline"],
                    createdAt=raw["createdAt"]
                )
                intents.append(dto)
        except Exception as e:
            logging.error(f"Failed to load user intent file {file}: {e}")
    return intents

def load_bids(directory: str) -> List[BidDTO]:
    bids = []
    for file in os.listdir(directory):
        if not file.startswith("bid_") or not file.endswith(".json"):
            continue
        path = os.path.join(directory, file)
        try:
            with open(path, 'r') as f:
                raw = json.load(f)
                dto = BidDTO(
                    bidHash=raw["bidHash"],
                    intentHash=raw["intentHash"],
                    solverAddress=raw["solverAddress"],
                    smartWalletAddress=raw["smartWalletAddress"],
                    status=raw["bidStatus"],
                    steps=raw["bid"]["steps"],
                    createdAt=raw["createdAt"]
                )
                bids.append(dto)
        except Exception as e:
            logging.error(f"Failed to load bid file {file}: {e}")
    return bids
