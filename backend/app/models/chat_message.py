from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from app.core.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_id = Column(String, index=True)

    # Message content
    message = Column(Text)
    response = Column(Text)

    # Metadata
    is_helpful = Column(Boolean, nullable=True)
    sources_used = Column(Text, nullable=True)  # JSON string of RAG sources

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
