from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.core.database import get_db
from app.models.chat_message import ChatMessage
from app.schemas.chatbot import ChatRequest, ChatResponse
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with the AI assistant about insurance terms and processes.
    Uses RAG (Retrieval-Augmented Generation) with Vertex AI.
    """
    # Initialize RAG service
    rag_service = RAGService()

    # Generate session ID if not provided
    session_id = chat_request.session_id or str(uuid.uuid4())

    try:
        # Get AI response using RAG
        result = await rag_service.generate_response(
            query=chat_request.message,
            user_id=chat_request.user_id,
            session_id=session_id
        )

        # Save chat message to database
        chat_message = ChatMessage(
            session_id=session_id,
            user_id=chat_request.user_id,
            message=chat_request.message,
            response=result["response"],
            sources_used=result.get("sources")
        )

        db.add(chat_message)
        db.commit()
        db.refresh(chat_message)

        return ChatResponse(
            session_id=session_id,
            message=chat_request.message,
            response=result["response"],
            sources=result.get("sources_list", []),
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )


@router.post("/feedback")
async def submit_feedback(
    message_id: int,
    is_helpful: bool,
    db: Session = Depends(get_db)
):
    """Submit feedback on a chat response"""
    chat_message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()

    if not chat_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found"
        )

    chat_message.is_helpful = is_helpful
    db.commit()

    return {"status": "success", "message": "Feedback submitted"}
