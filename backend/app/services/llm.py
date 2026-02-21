from groq import Groq
from openai import OpenAI
from app.core.config import settings
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMService:
    """LLM service with Groq (primary) and OpenAI (fallback)"""
    
    def __init__(self):
        groq_key = settings.GROQ_API_KEY
        openai_key = settings.OPENAI_API_KEY
        
        self.groq_client = Groq(api_key=groq_key) if groq_key else None
        
        self.openai_client = None
        if openai_key:
            try:
                self.openai_client = OpenAI(api_key=openai_key)
            except Exception as e:
                logger.warning(f"OpenAI client init failed (using Groq as primary): {e}")
    
    # Maps frontend service names to the action types the LLM should use
    SERVICE_ACTION_MAP = {
        'Gmail': 'send_email',
        'Google Calendar': 'create_calendar_event',
        'Google Meet': 'create_calendar_event',
        'Google Drive': 'create_google_doc',
        'Google Docs': 'create_google_doc',
        'Google Sheets': 'create_spreadsheet',
        'Notion': 'create_notion_page',
        'GitHub': 'create_github_issue',
        'Slack': 'send_slack_message',
    }

    def analyze_task(self, description: str, service_hint: str = None) -> dict:
        
        system_prompt = """You are a task analyzer for an AI automation platform. 
        Extract actionable steps from user requests. A single request can trigger MULTIPLE actions.
        
        Available actions:
        - send_email: {to, subject, body}
        - create_calendar_event: {summary, start_time (ISO format YYYY-MM-DDTHH:MM:SS), duration_minutes, attendees (list of valid emails only), description}
        - create_notion_page: {title, content (markdown)}
        - create_github_issue: {repo, title, body}
        - send_slack_message: {channel, text}
        - create_google_doc: {title, content}
        - create_spreadsheet: {title, data (2D array)}
        
        IMPORTANT RULES:
        1. If the user request involves MULTIPLE services, generate MULTIPLE actions in the actions array.
        2. For example "Schedule meeting and create notes and email team" should produce 3 actions.
        3. For calendar events, use ISO format for start_time (e.g., "2026-02-23T14:00:00").
        4. Only include attendees if valid email addresses are explicitly mentioned.
        5. Do NOT invent email addresses. If no email is specified, omit attendees.
        
        Respond ONLY with valid JSON in this format:
        {
            "actions": [{"type": "...", "parameters": {...}}, ...],
            "required_services": ["google", "notion", etc]
        }
        
        Be smart about extracting dates, times, email addresses, and generating appropriate content.
        For emails, write professional, concise messages based on the context.
        For calendar events, infer appropriate duration if not specified (default 60 minutes).
        """

        # If a service hint is provided, add a constraint but allow multi-action for complex requests
        if service_hint:
            required_action = self.SERVICE_ACTION_MAP.get(service_hint)
            if required_action:
                system_prompt += f"""
        
        The user initiated this from the "{service_hint}" service panel.
        The PRIMARY action MUST be "{required_action}".
        If the request involves additional services (e.g., also send email, also create Notion page), 
        include those as additional actions in the actions array.
        """
        
        # Add current date/time context so the LLM generates correct dates
        now = datetime.now()
        user_prompt = f"Current date and time: {now.strftime('%Y-%m-%d %H:%M')} (timezone: Asia/Kolkata, IST)\n\nUser request: {description}\n\nExtract actions:"
        
        try:
            if self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=2000
                )
                content = response.choices[0].message.content
            
            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3
                )
                content = response.choices[0].message.content
            
            else:
                logger.error("No LLM API key configured")
                return {"actions": [], "required_services": []}
            
            # Parse JSON response
            # Remove markdown code blocks if present
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            return json.loads(content)
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}\nContent: {content}")
            return {"actions": [], "required_services": []}
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            return {"actions": [], "required_services": []}
    
    def generate_email_body(self, purpose: str, context: str = "") -> str:
        """Generate professional email body"""
        
        prompt = f"""Write a professional, concise email.
        Purpose: {purpose}
        Context: {context}
        
        Write ONLY the email body (no subject line). Keep it brief and professional."""
        
        try:
            if self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            elif self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
        except:
            return "Hello,\n\n" + purpose + "\n\nBest regards"
