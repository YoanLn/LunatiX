from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.document import Document, DocumentType, VerificationStatus
from app.models.claim import Claim, ClaimStatus
from app.schemas.document import DocumentResponse
from app.services.document_verification import DocumentVerificationService
from app.services.storage_service import StorageService

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    claim_id: int = Form(...),
    document_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload and verify a document for a claim"""
    # Verify claim exists
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Claim not found"
        )

    # Validate document type
    try:
        doc_type = DocumentType(document_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid document type. Must be one of: {[e.value for e in DocumentType]}"
        )

    # Upload file to GCS
    storage_service = StorageService()
    file_content = await file.read()
    file_path = await storage_service.upload_file(
        file_content,
        file.filename,
        claim_id
    )

    # Create document record
    document = Document(
        claim_id=claim_id,
        document_type=doc_type,
        filename=file.filename,
        file_path=file_path,
        file_size=len(file_content),
        mime_type=file.content_type,
        verification_status=VerificationStatus.PENDING
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Trigger AI verification asynchronously
    verification_service = DocumentVerificationService()
    verification_result = await verification_service.verify_document(
        file_content,
        doc_type,
        file.content_type
    )

    # Update document with verification results
    document.verification_status = verification_result["status"]
    document.ai_analysis = verification_result["analysis"]
    document.confidence_score = verification_result["confidence_score"]
    document.is_compliant = verification_result["is_compliant"]
    document.compliance_issues = verification_result.get("compliance_issues")
    document.verified_at = datetime.utcnow()

    # Update claim status based on document verification
    if verification_result["is_compliant"]:
        claim.status = ClaimStatus.UNDER_REVIEW
        claim.status_message = "Documents received and verified. Claim is under review."
    else:
        claim.status = ClaimStatus.ADDITIONAL_INFO_REQUIRED
        claim.status_message = f"Document verification issues: {verification_result.get('compliance_issues')}"

    db.commit()
    db.refresh(document)

    return document


@router.get("/claim/{claim_id}", response_model=List[DocumentResponse])
async def get_claim_documents(claim_id: int, db: Session = Depends(get_db)):
    """Get all documents for a specific claim"""
    documents = db.query(Document).filter(Document.claim_id == claim_id).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get document details by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    document = db.query(Document).filter(Document.id == document_id).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Delete from storage
    storage_service = StorageService()
    await storage_service.delete_file(document.file_path)

    # Delete from database
    db.delete(document)
    db.commit()

    return None
