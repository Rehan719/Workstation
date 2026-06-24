import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ClientCommunityPlatform:
    """
    ARTICLE 222: Client Community Cultivation.
    Forums, webinars, and success stories to drive retention.
    """
    def __init__(self):
        self.forums = {} # topic: posts
        self.success_stories = []

    def post_to_forum(self, topic: str, content: str, client_id: str):
        if topic not in self.forums:
            self.forums[topic] = []
        self.forums[topic].append({"client_id": client_id, "content": content})
        logger.info(f"COMMUNITY: New post on {topic} from {client_id}.")

    def publish_success_story(self, client_id: str, impact_narrative: str):
        self.success_stories.append({"client_id": client_id, "narrative": impact_narrative})
        logger.info(f"COMMUNITY: Published success story for {client_id}.")

    def get_community_health(self) -> Dict[str, Any]:
        return {
            "forum_activity": sum(len(p) for p in self.forums.values()),
            "stories_published": len(self.success_stories)
        }
