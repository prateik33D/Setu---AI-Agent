import pytest
from app.models.task import Task, TaskStatus, TaskPriority
from app.agents.orchestrator import OrchestratorAgent


@pytest.fixture
def sample_task():
    from datetime import datetime
    return Task(
        id="test-task-1",
        user_id="user_abc",
        description="Send an email to test@example.com with subject Hello",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        action_items=[],
        assigned_agents=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )


def test_orchestrator_init():
    """Orchestrator can be instantiated."""
    o = OrchestratorAgent()
    assert o.llm_config is not None


@pytest.mark.asyncio
async def test_analyze_task_returns_dict(sample_task):
    """Analysis returns a dict with actions and required_services."""
    o = OrchestratorAgent()
    analysis = await o._analyze_task(sample_task.description)
    assert isinstance(analysis, dict)
    assert "actions" in analysis
    assert "required_services" in analysis
