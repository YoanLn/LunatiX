"""
Database initialization script.
Run this to create all tables in the database.
"""
from app.core.database import engine, Base
from app.models import Claim, Document, ChatMessage

def init_db():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("\nTables created:")
    print("- claims")
    print("- documents")
    print("- chat_messages")

if __name__ == "__main__":
    init_db()
