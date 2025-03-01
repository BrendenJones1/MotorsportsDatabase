import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

class GoogleDriveUploader:
    def __init__(self, credentials_path='credentials.json', token_path='token.pickle'):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file'] #change path to actual google drive path
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()
        
    def _authenticate(self):
        """Handles Google Drive authentication"""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
                
        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create new token if none exists
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, self.SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Save token
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        return build('drive', 'v3', credentials=creds)
    
    def create_folder(self, folder_name, parent_id=None):
        """Creates a folder in Google Drive"""
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            file_metadata['parents'] = [parent_id]
            
        folder = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        return folder.get('id')
    
    def upload_file(self, file_path, folder_id=None):
        """Uploads a file to Google Drive and returns file ID and webViewLink"""
        file_metadata = {
            'name': os.path.basename(file_path)
        }
        
        if folder_id:
            file_metadata['parents'] = [folder_id]
            
        media = MediaFileUpload(
            file_path,
            resumable=True
        )
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        
        return file.get('id'), file.get('webViewLink')

def get_file_type_id(cursor, file_extension):
    """Get file type ID from database, create if doesn't exist"""
    cursor.execute(
        "SELECT file_type_id FROM file_types WHERE extension = %s",
        (file_extension,)
    )
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    cursor.execute(
        "INSERT INTO file_types (extension, description) VALUES (%s, %s)",
        (file_extension, f"RaceStudio3 {file_extension} file")
    )
    return cursor.lastrowid

def save_file_info_to_db(cursor, session_id, file_path, file_id, web_link):
    """Save uploaded file information to database"""
    file_extension = os.path.splitext(file_path)[1][1:]  # Remove the dot
    file_type_id = get_file_type_id(cursor, file_extension)
    file_size = os.path.getsize(file_path)
    
    cursor.execute("""
        INSERT INTO session_files (
            session_id, file_type_id, file_name, cloud_storage_url,
            cloud_file_id, file_size_bytes, upload_date
        ) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    """, (
        session_id,
        file_type_id,
        os.path.basename(file_path),
        web_link,
        file_id,
        file_size
    ))
