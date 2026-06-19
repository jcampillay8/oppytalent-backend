import os
import io
import boto3
from botocore.exceptions import ClientError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime, timezone
import uuid

from app.config import settings
from app.models.usuario import Usuario

# --- Cloudflare R2 / AWS S3 Integration ---
def get_s3_client():
    if not settings.R2_ACCOUNT_ID:
        raise ValueError("R2_ACCOUNT_ID is not configured")
    
    return boto3.client(
        's3',
        endpoint_url=f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto"
    )

async def upload_to_r2(file_content: bytes, filename: str, content_type: str) -> str:
    """
    Sube un archivo a Cloudflare R2 y devuelve la URL pública.
    """
    s3_client = get_s3_client()
    bucket_name = settings.R2_BUCKET_NAME
    
    # Generar un nombre de archivo único para evitar colisiones
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    try:
        s3_client.upload_fileobj(
            io.BytesIO(file_content),
            bucket_name,
            unique_filename,
            ExtraArgs={"ContentType": content_type}
        )
        # La URL pública asume que el bucket tiene un dominio público configurado
        public_url = f"{settings.R2_PUBLIC_URL}/{unique_filename}"
        return public_url
    except ClientError as e:
        raise Exception(f"Error uploading to R2: {e}")


# File ending
