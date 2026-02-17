from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core.config import settings 
SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendarTool:
    def __init__(self, token_data: Optional[Dict] = None):
        self.creds = None
        pass

    def get_service(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        
        return build("calendar", "v3", credentials=creds)

    def list_events(self, max_results: int = 10):
        """Lists the next n events on the user's primary calendar."""
        try:
            service = self.get_service()
            now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            print(f"Getting the upcoming {max_results} events")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=max_results,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                return "No upcoming events found."

            result_str = ""
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                result_str += f"{start}: {event['summary']}\n"
            return result_str

        except HttpError as error:
            return f"An error occurred: {error}"

    def create_event(self, summary: str, start_time: str, end_time: str, description: str = ""):
        """
        Creates a new event.
        start_time and end_time should be ISO format strings (e.g., '2023-10-27T10:00:00').
        """
        try:
            service = self.get_service()
            event = {
                "summary": summary,
                "description": description,
                "start": {
                    "dateTime": start_time,
                    "timeZone": "UTC", 
                },
                "end": {
                    "dateTime": end_time,
                    "timeZone": "UTC",
                },
            }

            event = service.events().insert(calendarId="primary", body=event).execute()
            return f"Event created: {event.get('htmlLink')}"

        except HttpError as error:
            return f"An error occurred: {error}"
