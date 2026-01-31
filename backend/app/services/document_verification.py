import vertexai
from vertexai.generative_models import GenerativeModel, Part
import base64
from typing import Dict
from app.core.config import settings
from app.models.document import DocumentType, VerificationStatus


class DocumentVerificationService:
    """Service for AI-powered document verification using Vertex AI"""

    def __init__(self):
        vertexai.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.VERTEX_AI_LOCATION
        )
        self.model = GenerativeModel(settings.VERTEX_AI_MODEL_VISION)

    async def verify_document(
        self,
        file_content: bytes,
        document_type: DocumentType,
        mime_type: str
    ) -> Dict:
        """
        Verify a document using Vertex AI vision model.
        Returns verification status, analysis, and compliance information.
        """
        try:
            # Convert file to base64 if needed
            if mime_type.startswith("image/"):
                image_part = Part.from_data(file_content, mime_type=mime_type)
            else:
                # For PDFs, extract first page or convert to image
                image_part = Part.from_data(file_content, mime_type=mime_type)

            # Create prompt based on document type
            prompt = self._create_verification_prompt(document_type)

            # Generate analysis
            response = self.model.generate_content([prompt, image_part])

            # Parse response and determine compliance
            analysis = response.text
            compliance_result = self._analyze_compliance(analysis, document_type)

            return {
                "status": compliance_result["status"],
                "analysis": analysis,
                "confidence_score": compliance_result["confidence_score"],
                "is_compliant": compliance_result["is_compliant"],
                "compliance_issues": compliance_result.get("issues")
            }

        except Exception as e:
            return {
                "status": VerificationStatus.REJECTED,
                "analysis": f"Error during verification: {str(e)}",
                "confidence_score": 0,
                "is_compliant": False,
                "compliance_issues": "Verification failed due to technical error"
            }

    def _create_verification_prompt(self, document_type: DocumentType) -> str:
        """Create a verification prompt based on document type"""
        base_prompt = """
        You are an AI assistant helping to verify insurance claim documents.
        Analyze the provided document and provide a detailed assessment.
        """

        type_specific_prompts = {
            DocumentType.IDENTITY: """
            For this IDENTITY document:
            1. Verify it's a valid government-issued ID
            2. Check if the photo is clear and visible
            3. Verify if personal information (name, DOB, ID number) is legible
            4. Check expiration date if applicable
            5. Look for signs of tampering or forgery

            Provide a score from 0-100 for document quality and authenticity.
            List any issues found.
            """,
            DocumentType.MEDICAL_REPORT: """
            For this MEDICAL REPORT:
            1. Verify it's an official medical document
            2. Check for doctor/hospital letterhead
            3. Verify if diagnosis and treatment details are present
            4. Check if dates and signatures are visible
            5. Assess completeness of medical information

            Provide a score from 0-100 for document quality and completeness.
            List any missing information.
            """,
            DocumentType.INVOICE: """
            For this INVOICE:
            1. Verify it's an official invoice/receipt
            2. Check for business name and contact information
            3. Verify itemized charges are listed
            4. Check total amounts and dates
            5. Look for payment proof if applicable

            Provide a score from 0-100 for document validity.
            List any missing elements.
            """,
            DocumentType.POLICE_REPORT: """
            For this POLICE REPORT:
            1. Verify it's an official police/law enforcement document
            2. Check for case number and officer information
            3. Verify incident details and dates
            4. Check for official stamps or signatures
            5. Assess completeness of the report

            Provide a score from 0-100 for document authenticity.
            List any concerns.
            """,
            DocumentType.PROOF_OF_OWNERSHIP: """
            For this PROOF OF OWNERSHIP:
            1. Verify it's an official ownership document
            2. Check for owner name and property/item details
            3. Verify dates of purchase or registration
            4. Check for official seals or signatures
            5. Assess document legitimacy

            Provide a score from 0-100 for document validity.
            List any issues.
            """,
            DocumentType.PHOTOS: """
            For these PHOTOS:
            1. Verify images are clear and not blurry
            2. Check if damage/incident is clearly visible
            3. Verify multiple angles are shown if needed
            4. Check for date/time stamps if present
            5. Assess relevance to insurance claim

            Provide a score from 0-100 for photo quality and relevance.
            List any concerns.
            """,
            DocumentType.OTHER: """
            For this DOCUMENT:
            1. Identify what type of document this is
            2. Assess if it's relevant for an insurance claim
            3. Check for official markings or signatures
            4. Verify completeness and legibility
            5. Note any concerns about authenticity

            Provide a score from 0-100 for document quality.
            List any issues.
            """
        }

        return base_prompt + type_specific_prompts.get(
            document_type,
            type_specific_prompts[DocumentType.OTHER]
        )

    def _analyze_compliance(self, analysis: str, document_type: DocumentType) -> Dict:
        """
        Parse the AI analysis to determine compliance status.
        Extract confidence score and identify issues.
        """
        analysis_lower = analysis.lower()

        # Extract confidence score from analysis
        confidence_score = 0
        for word in analysis.split():
            if word.isdigit() and 0 <= int(word) <= 100:
                confidence_score = int(word)
                break

        # Determine compliance based on score and keywords
        issues = []
        is_compliant = False

        if confidence_score >= 80:
            status = VerificationStatus.VERIFIED
            is_compliant = True
        elif confidence_score >= 60:
            status = VerificationStatus.PARTIALLY_COMPLIANT
            is_compliant = False
            issues.append("Document quality is acceptable but has some concerns")
        else:
            status = VerificationStatus.REJECTED
            is_compliant = False
            issues.append("Document does not meet quality standards")

        # Look for specific issues in analysis
        if "blurry" in analysis_lower or "unclear" in analysis_lower:
            issues.append("Image quality is poor")
        if "missing" in analysis_lower:
            issues.append("Missing required information")
        if "expired" in analysis_lower:
            issues.append("Document may be expired")
        if "tamper" in analysis_lower or "forge" in analysis_lower:
            issues.append("Possible signs of tampering")

        return {
            "status": status,
            "confidence_score": confidence_score,
            "is_compliant": is_compliant,
            "issues": "; ".join(issues) if issues else None
        }
