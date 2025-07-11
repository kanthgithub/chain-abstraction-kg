import json
from dto import UserIntentDTO, BidDTO

class GraphBuilder:
    def __init__(self, db):
        self.db = db

    def insert_user_intent(self, dto: UserIntentDTO):
        self.db.run_query("""
            MERGE (a:Account {address: $account})
            MERGE (i:UserIntent {intentHash: $intentHash})
            SET i.intentStatus = $intentStatus,
                i.slippage = $slippage,
                i.deadline = $deadline,
                i.createdAt = $createdAt,
                i.rawJson = $rawJson
            MERGE (a)-[:PLACED]->(i)
        """, {
            "account": dto.account,
            "intentHash": dto.intentHash,
            "intentStatus": dto.intentStatus,
            "slippage": dto.slippage,
            "deadline": dto.deadline,
            "createdAt": dto.createdAt,
            "rawJson": json.dumps(dto.dict())
        })

        for asset in dto.dispensableAssets:
            self.db.run_query("""
                MERGE (t:Token {address: $asset})
                MERGE (i:UserIntent {intentHash: $intentHash})
                MERGE (i)-[:USES_ASSET]->(t)
            """, {"intentHash": dto.intentHash, "asset": asset.asset})

        for asset in dto.desiredAssets:
            self.db.run_query("""
                MERGE (t:Token {address: $asset})
                MERGE (i:UserIntent {intentHash: $intentHash})
                MERGE (i)-[:DESIRES_ASSET]->(t)
            """, {"intentHash": dto.intentHash, "asset": asset.asset})

    def insert_bid(self, dto: BidDTO):
        self.db.run_query("""
            MERGE (s:Solver {address: $solver})
            MERGE (b:Bid {bidHash: $bidHash})
            SET b.status = $status,
                b.createdAt = $createdAt,
                b.rawJson = $rawJson
            MERGE (s)-[:RESPONDED_WITH]->(b)
            MERGE (b)-[:BID_FOR]->(:UserIntent {intentHash: $intentHash})
        """, {
            "bidHash": dto.bidHash,
            "solver": dto.solverAddress,
            "status": dto.status,
            "createdAt": dto.createdAt,
            "intentHash": dto.intentHash,
            "rawJson": json.dumps(dto.dict())
        })

        for step in dto.steps:
            path = step.solution.get("path", {})
            if not path:
                continue
            self.db.run_query("""
                MERGE (c:Token {address: $tokenConsumed})
                MERGE (r:Token {address: $tokenReceived})
                MERGE (b:Bid {bidHash: $bidHash})
                MERGE (b)-[:TRANSFER_STEP {
                    sequence: $seq,
                    action: $action,
                    amount: $amount
                }]->(r)
            """, {
                "bidHash": dto.bidHash,
                "tokenConsumed": path.get("tokenConsumed"),
                "tokenReceived": path.get("tokenReceived"),
                "seq": step.sequenceNumber,
                "action": path.get("action"),
                "amount": path.get("amountConsumed")
            })
