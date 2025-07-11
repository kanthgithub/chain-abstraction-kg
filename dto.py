from pydantic import BaseModel
from typing import List, Optional

class PermittedAccount(BaseModel):
    account: str
    chainId: int

class Asset(BaseModel):
    asset: str
    chainId: int
    value: Optional[str] = None
    maxValue: Optional[str] = None

class UserIntentDTO(BaseModel):
    intentHash: str
    intentStatus: str
    account: str
    permittedAccounts: List[PermittedAccount]
    desiredAssets: List[Asset]
    dispensableAssets: List[Asset]
    slippage: float
    deadline: int
    createdAt: str

class BidStep(BaseModel):
    chainId: int
    sequenceNumber: int
    solution: dict

class BidDTO(BaseModel):
    bidHash: str
    intentHash: str
    solverAddress: str
    smartWalletAddress: str
    status: str
    steps: List[BidStep]
    createdAt: str
