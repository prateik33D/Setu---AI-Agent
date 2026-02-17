from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)

class SheetsService:
    """Google Sheets operations"""
    
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
        
        self.service = build('sheets', 'v4', credentials=creds)
    
    def create_spreadsheet(self, title: str, data: list = None) -> dict:
        """Create Google Sheet"""
        try:
            spreadsheet = {'properties': {'title': title}}
            result = self.service.spreadsheets().create(body=spreadsheet).execute()
            
            if data:
                self.service.spreadsheets().values().update(
                    spreadsheetId=result['spreadsheetId'],
                    range='Sheet1!A1',
                    valueInputOption='RAW',
                    body={'values': data}
                ).execute()
            
            return {
                "spreadsheet_id": result['spreadsheetId'],
                "url": result['spreadsheetUrl'],
                "status": "created"
            }
        except Exception as e:
            logger.error(f"Failed to create sheet: {e}")
            raise
