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


# --- Google Drive Integration ---
def get_drive_service(user: Usuario):
    if not user.google_refresh_token:
        raise ValueError("Usuario no ha conectado su cuenta de Google Drive")
        
    creds = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
    )
    
    return build('drive', 'v3', credentials=creds)

async def get_or_create_oppytalent_folder(drive_service) -> str:
    """Busca la carpeta OppyTalent en la raíz del Drive del usuario. Si no existe, la crea."""
    folder_name = "OppyTalent"
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if not items:
        # Create folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = drive_service.files().create(body=file_metadata, fields='id').execute()
        
        # Make the folder public so the proxy can read the images
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        drive_service.permissions().create(fileId=folder.get('id'), body=permission).execute()
        
        return folder.get('id')
    
    return items[0].get('id')

async def upload_to_google_drive(user: Usuario, file_content: bytes, filename: str, content_type: str) -> str:
    """
    Sube un archivo a la carpeta OppyTalent del Google Drive del usuario.
    Devuelve la URL pública del visor de Drive.
    """
    drive_service = get_drive_service(user)
    
    folder_id = await get_or_create_oppytalent_folder(drive_service)
    
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    
    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype=content_type, resumable=True)
    
    file = drive_service.files().create(
        body=file_metadata, 
        media_body=media,
        fields='id, webViewLink'
    ).execute()
    
    # Devuelve el link público. El frontend lo parseará con `parseImageUrl`
    return f"https://drive.google.com/file/d/{file.get('id')}/view"
