from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.claim import ClaimStatus


class ClaimCreate(BaseModel):
    user_id: str
    claim_type: str
    description: str
    claim_amount: float = Field(gt=0)


class ClaimStatusUpdate(BaseModel):
    status: ClaimStatus
    status_message: Optional[str] = None


class ClaimResponse(BaseModel):
    id: int
    claim_number: str
    user_id: str
    claim_type: str
    description: str
    claim_amount: float
    status: ClaimStatus
    status_message: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
