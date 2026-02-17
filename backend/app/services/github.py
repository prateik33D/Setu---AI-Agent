from github import Github
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    def __init__(self, access_token: str):
        self.client = Github(access_token)
    
    def create_issue(self, repo: str, title: str, body: str = "", labels: list = None) -> dict:
        try:
            repository = self.client.get_repo(repo)
            issue = repository.create_issue(
                title=title,
                body=body,
                labels=labels or []
            )
            
            return {
                "issue_number": issue.number,
                "url": issue.html_url,
                "status": "created"
            }
        except Exception as e:
            logger.error(f"Failed to create issue: {e}")
            raise
