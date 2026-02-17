from notion_client import Client
import logging

logger = logging.getLogger(__name__)

class NotionService:
    """Notion operations"""
    
    def __init__(self, access_token: str):
        self.client = Client(auth=access_token)
    
    def create_page(self, title: str, content: str = "", parent_page_id: str = None) -> dict:
        try:
            if parent_page_id:
                parent = {"type": "page_id", "page_id": parent_page_id}
            else:
                try:
                    search_result = self.client.search(
                        filter={"property": "object", "value": "page"},
                        page_size=1
                    )
                    pages = search_result.get("results", [])
                    if pages:
                        parent = {"type": "page_id", "page_id": pages[0]["id"]}
                    else:
                        raise Exception(
                            "No Notion pages accessible. Please share a Notion page with your SETU integration first: "
                            "Open Notion → Find a page → Click '...' → Add connections → Select SETU"
                        )
                except Exception as search_err:
                    if "No Notion pages accessible" in str(search_err):
                        raise
                    raise Exception(f"Notion search failed: {search_err}")

            page = self.client.pages.create(
                parent=parent,
                properties={
                    "title": {"title": [{"text": {"content": title}}]}
                }
            )

            if content:
                blocks = []
                for paragraph in content.split('\n\n'):
                    if paragraph.strip():
                        blocks.append({
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": paragraph[:2000]}}]
                            }
                        })

                if blocks:
                    self.client.blocks.children.append(
                        block_id=page['id'],
                        children=blocks[:100]  # Notion limit
                    )

            return {
                "page_id": page['id'],
                "url": page.get('url', f"https://notion.so/{page['id'].replace('-', '')}"),
                "status": "created",
                "title": title
            }
        except Exception as e:
            logger.error(f"Failed to create Notion page: {e}")
            raise
