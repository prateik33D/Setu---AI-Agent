from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import select
from typing import Optional, Dict
from cryptography.fernet import Fernet
import os
from app.models.integration import DBIntegration, IntegrationStatus

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./setu.db")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Token encryption
from app.core.config import settings

# Token encryption
ENCRYPTION_KEY = settings.ENCRYPTION_KEY
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"WARNING: Generated new ENCRYPTION_KEY. Add this to .env: {ENCRYPTION_KEY}")

if isinstance(ENCRYPTION_KEY, str):
    ENCRYPTION_KEY = ENCRYPTION_KEY.encode()

cipher = Fernet(ENCRYPTION_KEY)

def encrypt_token(token: str) -> str:
    """Encrypt access token"""
    if not token:
        return ""
    return cipher.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    """Decrypt access token"""
    if not encrypted_token:
        return ""
    return cipher.decrypt(encrypted_token.encode()).decode()

async def get_user_credentials(user_id: str, service_type: str) -> Optional[Dict]:
    """Get decrypted credentials for a user's service integration"""
    async with AsyncSessionLocal() as session:
        query = select(DBIntegration).where(
            DBIntegration.user_id == user_id,
            DBIntegration.service_type == service_type,
            DBIntegration.status == IntegrationStatus.CONNECTED
        )
        result = await session.execute(query)
        integration = result.scalar_one_or_none()
        
        if not integration:
            return None
        
        return {
            "access_token": decrypt_token(integration.access_token),
            "refresh_token": decrypt_token(integration.refresh_token) if integration.refresh_token else None,
            "token_expiry": integration.token_expiry,
            "scopes": integration.scopes or []
        }

async def save_user_credentials(
    user_id: str,
    service_name: str,
    service_type: str,
    access_token: str,
    refresh_token: Optional[str] = None,
    expires_in: int = 3600,
    scopes: list = None
):
    """Save encrypted credentials to database"""
    from datetime import datetime, timedelta
    import uuid
    
    async with AsyncSessionLocal() as session:
        # Check if integration already exists
        query = select(DBIntegration).where(
            DBIntegration.user_id == user_id,
            DBIntegration.service_name == service_name
        )
        result = await session.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing
            existing.access_token = encrypt_token(access_token)
            if refresh_token:
                existing.refresh_token = encrypt_token(refresh_token)
            existing.token_expiry = datetime.utcnow() + timedelta(seconds=expires_in)
            existing.status = IntegrationStatus.CONNECTED
            existing.scopes = scopes or []
            existing.updated_at = datetime.utcnow()
        else:
            # Create new
            integration = DBIntegration(
                id=str(uuid.uuid4()),
                user_id=user_id,
                service_type=service_type,
                service_name=service_name,
                status=IntegrationStatus.CONNECTED,
                access_token=encrypt_token(access_token),
                refresh_token=encrypt_token(refresh_token) if refresh_token else None,
                token_expiry=datetime.utcnow() + timedelta(seconds=expires_in),
                scopes=scopes or [],
                connected_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(integration)
        
        await session.commit()

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        from app.models.integration import Base
        await conn.run_sync(Base.metadata.create_all)
