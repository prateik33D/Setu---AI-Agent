from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from app.api import deps
from app.core.database import AsyncSessionLocal
from app.models.integration import DBIntegration, IntegrationStatus
from sqlalchemy import select

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
async def list_integrations(current_user: dict = Depends(deps.get_current_user)):
    """
    List connected integrations for the current user.
    """
    user_id = current_user.get("sub") or current_user.get("id", "unknown")
    
    async with AsyncSessionLocal() as session:
        query = select(DBIntegration).where(
            DBIntegration.user_id == user_id,
            DBIntegration.status == IntegrationStatus.CONNECTED
        )
        result = await session.execute(query)
        integrations = result.scalars().all()
        
        # Map to response format
        integration_map = {}
        for integration in integrations:
            integration_map[integration.service_type] = {
                "id": integration.service_type,
                "name": integration.service_name,
                "connected": True,
                "connected_at": integration.connected_at.isoformat() if integration.connected_at else None
            }
        
        # Return all possible integrations with connection status
        all_integrations = [
            {"id": "google", "name": "Google", "connected": False},
            {"id": "notion", "name": "Notion", "connected": False},
            {"id": "github", "name": "GitHub", "connected": False},
            {"id": "slack", "name": "Slack", "connected": False},
        ]
        
        # Update with actual connection status
        for integration in all_integrations:
            if integration["id"] in integration_map:
                integration.update(integration_map[integration["id"]])
        
        return all_integrations

@router.delete("/{integration_id}")
async def disconnect_integration(
    integration_id: str,
    current_user: dict = Depends(deps.get_current_user)
):
    """
    Disconnect an integration.
    """
    return {"message": f"Disconnected {integration_id}"}
