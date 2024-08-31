from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
load_dotenv()
import os

UPLOAD_FOLDER  = os.getenv("UPLOAD_FOLDER")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# 建立憑證
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# 串連服務
service = build('drive', 'v3', credentials=creds)

def upload_to_drive(file_path, folder_id=UPLOAD_FOLDER):
    file_name = os.path.basename(file_path)
    
    # Metadata for the file
    file_metadata = {
        'name': file_name,
        'parents': [folder_id] if folder_id else None
    }

    media = MediaFileUpload(file_path, resumable=True)

    # Upload the file
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Make the file publicly accessible
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(
        fileId=file.get('id'),
        body=permission
    ).execute()

    # Get the file's web link
    file = service.files().get(fileId=file.get('id'), fields='webViewLink').execute()

    return file.get('webViewLink')

upload_to_drive('/Users/ponfu/Desktop/vs code/MusicCreation/front-end/music-app/src/assets/song-cover.jpg', UPLOAD_FOLDER)
