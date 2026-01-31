from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "LunatiX Insurance Platform"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # Google Cloud
    GOOGLE_CLOUD_PROJECT: str = ""
    VERTEX_AI_LOCATION: str = "us-central1"
    GCS_BUCKET_NAME: str = ""
    GOOGLE_APPLICATION_CREDENTIALS: str = ""

    # Database
    DATABASE_URL: str = "sqlite:///./insurance.db"

    # Security
    SECRET_KEY: str = "change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    # Vertex AI Models
    VERTEX_AI_MODEL_VISION: str = "gemini-1.5-flash"
    VERTEX_AI_MODEL_TEXT: str = "gemini-1.5-flash"
    VERTEX_AI_EMBEDDING_MODEL: str = "text-embedding-004"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
