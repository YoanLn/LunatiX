from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class DocumentType(str, enum.Enum):
    IDENTITY = "identity"
    MEDICAL_REPORT = "medical_report"
    INVOICE = "invoice"
    POLICE_REPORT = "police_report"
    PROOF_OF_OWNERSHIP = "proof_of_ownership"
    PHOTOS = "photos"
    OTHER = "other"


class VerificationStatus(str, enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    PARTIALLY_COMPLIANT = "partially_compliant"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))

    # Document details
    document_type = Column(Enum(DocumentType))
    filename = Column(String)
    file_path = Column(String)  # GCS path
    file_size = Column(Integer)
    mime_type = Column(String)

    # AI Verification
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    ai_analysis = Column(Text, nullable=True)
    confidence_score = Column(Integer, nullable=True)  # 0-100
    is_compliant = Column(Boolean, default=False)
    compliance_issues = Column(Text, nullable=True)

    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)

    # Relationships
    claim = relationship("Claim", back_populates="documents")
