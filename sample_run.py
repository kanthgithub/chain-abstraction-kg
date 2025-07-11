from ingestor import ingest_pipeline
import json

# Paste your JSONs here
user_intent_json = """{
        "intentHash": "0x0ed5c65e5ef42fa996298fcb22592f3be1b44b1dfd6edba839879463f554838e",
        "intentStatus": "BID_SUBMITTED",
        "userIntent": {
            "intentHash": "0x0ed5c65e5ef42fa996298fcb22592f3be1b44b1dfd6edba839879463f554838e",
            "core": {
                "permittedAccounts": [
                    {
                        "account": "0x23F04522a2ec5a8b188C48c18edAE54005b537a3",
                        "chainId": 8453
                    }
                ]
            },
            "constraints": {
                "permittedChains": [
                    42161
                ],
                "deadline": 1751304211,
                "maxGas": 6000000,
                "slippagePercentage": 5.0,
                "desiredAssets": [
                    {
                        "asset": "0xfdfff924c413a228c9fc62b1978ed8f755d81111",
                        "value": "500000000000000000000",
                        "chainId": 8453
                    }
                ],
                "dispensableAssets": [
                    {
                        "asset": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
                        "maxValue": "100000",
                        "chainId": 42161
                    }
                ]
            }
        },
        "account": "0x448b47F358dA18749529bDeAeC26322E58D13177",
        "createdAt": "2025-06-30T17:22:33.914788126",
        "createdAtEpoch": 1751304153,
        "updatedAt": "2025-06-30T17:22:36.785395867",
        "updatedAtEpoch": 1751304156
    }"""

bid_json = """[
    {
        "bidHash": "0xc999e8523aa6400c4d2421e26ab51d8100f6a3df83b1ccbdfcf8a04b91129baf",
        "smartWalletAddress": "0x23F04522a2ec5a8b188C48c18edAE54005b537a3",
        "solverAddress": "0x7C84F10502FcDea2E403b70feA96a4aE990a34DF",
        "intentHash": "0x0ed5c65e5ef42fa996298fcb22592f3be1b44b1dfd6edba839879463f554838e",
        "bid": {
            "bidHash": "0xc999e8523aa6400c4d2421e26ab51d8100f6a3df83b1ccbdfcf8a04b91129baf",
            "solverAddress": "0x7C84F10502FcDea2E403b70feA96a4aE990a34DF",
            "intentHash": "0x0ed5c65e5ef42fa996298fcb22592f3be1b44b1dfd6edba839879463f554838e",
            "steps": [
                {
                    "sequenceNumber": 1,
                    "chainId": 8453,
                    "validUntil": 1751314956,
                    "solution": {
                        "to": "0xfdfff924c413a228c9fc62b1978ed8f755d81111",
                        "callData": "0xa9059cbb00000000000000000000000023f04522a2ec5a8b188c48c18edae54005b537a300000000000000000000000000000000000000000000001b1ae4d6e2ef500000",
                        "value": "0",
                        "path": {
                            "tokenConsumed": "0xfdfff924c413a228c9fc62b1978ed8f755d81111",
                            "amountConsumed": "500000000000000000000",
                            "tokenReceived": "0xfdfff924c413a228c9fc62b1978ed8f755d81111",
                            "amountReceived": "500000000000000000000",
                            "action": "TRANSFER"
                        }
                    }
                }
            ]
        },
        "bidStatus": "PENDING",
        "createdAt": "2025-06-30T17:22:36.791050721",
        "createdAtEpoch": 1751304156,
        "updatedAt": "2025-06-30T17:22:36.791050721",
        "updatedAtEpoch": 1751304156,
        "executedAtEpoch": 0,
        "message": "",
        "executedTransactions": []
    }
]"""

user_intent = json.loads(user_intent_json)
bids = json.loads(bid_json)

ingest_pipeline(user_intent, bids)