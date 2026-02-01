from google.cloud import storage
from app.core.config import settings
import os
from datetime import datetime
import uuid


class StorageService:
    """Service for handling file uploads to Google Cloud Storage"""

    def __init__(self):
        self.client = storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)
        self.bucket_name = settings.GCS_BUCKET_NAME

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        claim_id: int
    ) -> str:
        """
        Upload a file to GCS and return the file path.
        Files are organized by claim_id and timestamped.
        """
        try:
            bucket = self.client.bucket(self.bucket_name)

            # Create unique filename with timestamp
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_extension = os.path.splitext(filename)[1]
            blob_name = f"claims/{claim_id}/{timestamp}_{unique_id}{file_extension}"

            # Upload file
            blob = bucket.blob(blob_name)
            blob.upload_from_string(file_content)

            return blob_name

        except Exception as e:
            # For development without GCS, save locally
            if settings.DEBUG:
                local_path = f"./uploads/claims/{claim_id}"
                os.makedirs(local_path, exist_ok=True)

                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                unique_id = str(uuid.uuid4())[:8]
                file_extension = os.path.splitext(filename)[1]
                local_file = f"{local_path}/{timestamp}_{unique_id}{file_extension}"

                with open(local_file, "wb") as f:
                    f.write(file_content)

                return local_file
            else:
                raise Exception(f"Failed to upload file: {str(e)}")

    async def delete_file(self, file_path: str) -> bool:
        """Delete a file from GCS"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(file_path)
            blob.delete()
            return True

        except Exception as e:
            # For development, delete local file
            if settings.DEBUG and os.path.exists(file_path):
                os.remove(file_path)
                return True
            else:
                raise Exception(f"Failed to delete file: {str(e)}")

    async def get_file_url(self, file_path: str, expiration_minutes: int = 60) -> str:
        """Get a signed URL for accessing a file"""
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(file_path)

            url = blob.generate_signed_url(
                expiration=expiration_minutes * 60,
                method="GET"
            )

            return url

        except Exception as e:
            if settings.DEBUG:
                # Return local file path for development
                return f"file://{os.path.abspath(file_path)}"
            else:
                raise Exception(f"Failed to generate file URL: {str(e)}")

    async def get_gcs_uri_url(self, gcs_uri: str, expiration_minutes: int = 60) -> str:
        """Get a signed URL for a GCS URI (gs://bucket/path)."""
        if not gcs_uri.startswith("gs://"):
            raise ValueError("Invalid GCS URI")

        parts = gcs_uri[5:].split("/", 1)
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError("Invalid GCS URI")

        bucket_name, blob_name = parts

        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            url = blob.generate_signed_url(
                expiration=expiration_minutes * 60,
                method="GET"
            )

            return url

        except Exception as e:
            if settings.DEBUG:
                return f"https://storage.googleapis.com/{bucket_name}/{blob_name}"
            else:
                raise Exception(f"Failed to generate file URL: {str(e)}")
