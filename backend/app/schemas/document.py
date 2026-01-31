from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.document import DocumentType, VerificationStatus


class DocumentResponse(BaseModel):
    id: int
    claim_id: int
    document_type: DocumentType
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    verification_status: VerificationStatus
    ai_analysis: Optional[str]
    confidence_score: Optional[int]
    is_compliant: bool
    compliance_issues: Optional[str]
    uploaded_at: datetime
    verified_at: Optional[datetime]

    class Config:
        from_attributes = True
