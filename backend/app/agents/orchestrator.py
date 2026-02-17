from typing import Dict, Any
from app.services.llm import LLMService
from app.services.google.gmail import GmailService
from app.services.google.calendar import CalendarService
from app.services.google.docs import DocsService
from app.services.google.sheets import SheetsService
from app.services.notion import NotionService
from app.services.github import GitHubService
from app.services.slack import SlackService
from app.core.database import get_user_credentials
import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent:
    def __init__(self):
        self.llm = LLMService()
    
    async def process_task(self, task_description: str, user_id: str) -> Dict[str, Any]:
        """
        Process user task end-to-end:
        1. Analyze with LLM to extract actions
        2. Execute each action using appropriate service
        3. Return results
        """
        
        logger.info(f"Processing task for user {user_id}: {task_description}")
        
        # Step 1: Analyze task
        analysis = self.llm.analyze_task(task_description)
        
        if not analysis.get('actions'):
            return {
                "status": "failed",
                "message": "Could not understand the task",
                "results": []
            }
        
        
        results = []
        
        for action in analysis['actions']:
            try:
                result = await self._execute_action(action, user_id)
                results.append({
                    "action": action['type'],
                    "status": "success",
                    "result": result
                })
            except Exception as e:
                logger.error(f"Action {action['type']} failed: {e}")
                results.append({
                    "action": action['type'],
                    "status": "failed",
                    "error": str(e)
                })
        
        return {
            "status": "completed",
            "analysis": analysis,
            "results": results
        }
    
    async def _execute_action(self, action: Dict, user_id: str) -> Dict:
        """Execute a single action"""
        
        action_type = action['type']
        params = action['parameters']
        
        # EMAIL
        if action_type == 'send_email':
            creds = await get_user_credentials(user_id, 'google')
            if not creds:
                raise Exception("Google account not connected")
            
            gmail = GmailService(creds['access_token'], creds.get('refresh_token'))
            return gmail.send_email(
                to=params['to'],
                subject=params.get('subject', 'No Subject'),
                body=params.get('body', ''),
                cc=params.get('cc')
            )
        
        # CALENDAR
        elif action_type == 'create_calendar_event':
            creds = await get_user_credentials(user_id, 'google')
            if not creds:
                raise Exception("Google account not connected")
            
            calendar = CalendarService(creds['access_token'], creds.get('refresh_token'))
            return calendar.create_event(
                summary=params['summary'],
                start_time=params['start_time'],
                duration_minutes=params.get('duration_minutes', 60),
                attendees=params.get('attendees'),
                description=params.get('description', '')
            )
        
        # GOOGLE DOCS
        elif action_type == 'create_google_doc':
            creds = await get_user_credentials(user_id, 'google')
            if not creds:
                raise Exception("Google account not connected")
            
            docs = DocsService(creds['access_token'], creds.get('refresh_token'))
            return docs.create_document(
                title=params['title'],
                content=params.get('content', '')
            )
        
        # GOOGLE SHEETS
        elif action_type == 'create_spreadsheet':
            creds = await get_user_credentials(user_id, 'google')
            if not creds:
                raise Exception("Google account not connected")
            
            sheets = SheetsService(creds['access_token'], creds.get('refresh_token'))
            return sheets.create_spreadsheet(
                title=params['title'],
                data=params.get('data')
            )
        
        # NOTION
        elif action_type == 'create_notion_page':
            creds = await get_user_credentials(user_id, 'notion')
            if not creds:
                raise Exception("Notion account not connected")
            
            notion = NotionService(creds['access_token'])
            return notion.create_page(
                title=params['title'],
                content=params.get('content', '')
            )
        
        # GITHUB
        elif action_type == 'create_github_issue':
            creds = await get_user_credentials(user_id, 'github')
            if not creds:
                raise Exception("GitHub account not connected")
            
            github = GitHubService(creds['access_token'])
            return github.create_issue(
                repo=params['repo'],
                title=params['title'],
                body=params.get('body', ''),
                labels=params.get('labels')
            )
        
        # SLACK
        elif action_type == 'send_slack_message':
            creds = await get_user_credentials(user_id, 'slack')
            if not creds:
                raise Exception("Slack account not connected")
            
            slack = SlackService(creds['access_token'])
            return slack.send_message(
                channel=params.get('channel', '#general'),
                text=params.get('text', params.get('message', ''))
            )
        
        else:
            raise Exception(f"Unknown action type: {action_type}")
