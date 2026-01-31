from sqlalchemy import Column, Integer, String, DateTime, Enum, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class ClaimStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    DOCUMENTS_PENDING = "documents_pending"
    UNDER_REVIEW = "under_review"
    ADDITIONAL_INFO_REQUIRED = "additional_info_required"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String, unique=True, index=True)
    user_id = Column(String, index=True)

    # Claim details
    claim_type = Column(String)  # health, auto, home, life, etc.
    description = Column(Text)
    claim_amount = Column(Float)

    # Status tracking
    status = Column(Enum(ClaimStatus), default=ClaimStatus.SUBMITTED)
    status_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    documents = relationship("Document", back_populates="claim", cascade="all, delete-orphan")
