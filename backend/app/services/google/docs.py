from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)

class DocsService:
    """Google Docs operations"""
    
    def __init__(self, access_token: str, refresh_token: str = None):
        from google.auth.transport.requests import Request
        import os
        
        creds = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        )
        
        # Auto-refresh if expired
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        self.service = build('docs', 'v1', credentials=creds)
    
    def create_document(self, title: str, content: str = "") -> dict:
        """Create Google Doc"""
        try:
            doc = self.service.documents().create(body={'title': title}).execute()
            
            if content:
                requests = [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }]
                
                self.service.documents().batchUpdate(
                    documentId=doc['documentId'],
                    body={'requests': requests}
                ).execute()
            
            return {
                "document_id": doc['documentId'],
                "title": title,
                "url": f"https://docs.google.com/document/d/{doc['documentId']}/edit",
                "status": "created"
            }
        except Exception as e:
            logger.error(f"Failed to create doc: {e}")
            raise
