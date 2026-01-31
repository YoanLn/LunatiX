from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from app.core.database import get_db
from app.models.claim import Claim, ClaimStatus
from app.schemas.claim import ClaimCreate, ClaimResponse, ClaimStatusUpdate

router = APIRouter()


@router.post("/", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
async def create_claim(
    claim_data: ClaimCreate,
    db: Session = Depends(get_db)
):
    """Create a new insurance claim"""
    # Generate unique claim number
    claim_number = f"CLM-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"

    claim = Claim(
        claim_number=claim_number,
        user_id=claim_data.user_id,
        claim_type=claim_data.claim_type,
        description=claim_data.description,
        claim_amount=claim_data.claim_amount,
        status=ClaimStatus.SUBMITTED,
        status_message="Claim submitted successfully. Please upload required documents."
    )

    db.add(claim)
    db.commit()
    db.refresh(claim)

    return claim


@router.get("/{claim_id}", response_model=ClaimResponse)
async def get_claim(claim_id: int, db: Session = Depends(get_db)):
    """Get claim details by ID"""
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )

    return claim


@router.get("/user/{user_id}", response_model=List[ClaimResponse])
async def get_user_claims(user_id: str, db: Session = Depends(get_db)):
    """Get all claims for a specific user"""
    claims = db.query(Claim).filter(Claim.user_id == user_id).order_by(Claim.created_at.desc()).all()
    return claims


@router.get("/", response_model=List[ClaimResponse])
async def list_claims(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all claims (admin endpoint)"""
    claims = db.query(Claim).offset(skip).limit(limit).all()
    return claims


@router.patch("/{claim_id}/status", response_model=ClaimResponse)
async def update_claim_status(
    claim_id: int,
    status_update: ClaimStatusUpdate,
    db: Session = Depends(get_db)
):
    """Update claim status"""
    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )

    claim.status = status_update.status
    if status_update.status_message:
        claim.status_message = status_update.status_message

    db.commit()
    db.refresh(claim)

    return claim
