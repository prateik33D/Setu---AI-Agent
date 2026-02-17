from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class GmailService:
    """Gmail operations"""
    
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
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def send_email(self, to: str, subject: str, body: str, cc: list = None) -> dict:
        """Send email via Gmail"""
        try:
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            if cc:
                message['cc'] = ', '.join(cc)
            
            message.attach(MIMEText(body, 'plain'))
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            result = self.service.users().messages().send(
                userId='me',
                body={'raw': raw}
            ).execute()
            
            logger.info(f"Email sent: {result['id']}")
            
            return {
                "message_id": result['id'],
                "status": "sent",
                "to": to,
                "subject": subject
            }
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise Exception(f"Gmail send failed: {str(e)}")
