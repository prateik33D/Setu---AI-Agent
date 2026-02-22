from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SETU"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  
        "http://localhost:3000",  
    ]

    # Auth
    CLERK_SECRET_KEY: str = "sk_test_..." 
    CLERK_PUBLISHABLE_KEY: str = "pk_test_..." 

    # Google
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str | None = None

    # Notion
    NOTION_CLIENT_ID: str | None = None
    NOTION_CLIENT_SECRET: str | None = None
    NOTION_REDIRECT_URI: str | None = None

    # GitHub
    GITHUB_CLIENT_ID: str | None = None
    GITHUB_CLIENT_SECRET: str | None = None

    # Slack
    SLACK_CLIENT_ID: str | None = None
    SLACK_CLIENT_SECRET: str | None = None
    SLACK_SIGNING_SECRET: str | None = None

    # Discord
    DISCORD_BOT_TOKEN: str | None = None
    DISCORD_WEBHOOK_URL: str | None = None

    # AI
    GROQ_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    
    # Encryption
    ENCRYPTION_KEY: str | None = None
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./setu.db"

    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

settings = Settings()
