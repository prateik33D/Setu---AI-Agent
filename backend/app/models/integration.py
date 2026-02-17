from enum import Enum
from sqlalchemy import Column, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Optional

Base = declarative_base()

class IntegrationType(str, Enum):
    GOOGLE = "google"
    NOTION = "notion"
    GITHUB = "github"
    SLACK = "slack"

class IntegrationStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"

class DBIntegration(Base):
    __tablename__ = "integrations"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    service_type = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
    status = Column(String, nullable=False, default=IntegrationStatus.CONNECTED)
    access_token = Column(Text, nullable=False)  # Encrypted
    refresh_token = Column(Text, nullable=True)  # Encrypted
    token_expiry = Column(DateTime, nullable=True)
    scopes = Column(JSON, nullable=True)
    connected_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
