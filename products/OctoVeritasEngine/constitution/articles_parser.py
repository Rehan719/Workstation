import re
import json
import os

class ConstitutionParser:
    def __init__(self, md_path: str = "agentic_core/constitution/CONSTITUTION_v138.0.0.md"):
        self.md_path = md_path
        self.cache_path = os.path.join(os.path.dirname(__file__), "articles_cache.json")

    def parse_and_cache(self) -> dict:
        if not os.path.exists(self.md_path):
            return {}

        with open(self.md_path, 'r') as f:
            content = f.read()

        # Regex for Articles 1–1095
        pattern = r"### Article (\d+) – (.+?)\n\n(.*?)(?=\n### Article |\Z)"
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

        articles = {}
        for match in matches:
            article_id = match.group(1)
            title = match.group(2).strip()
            text = match.group(3).strip()
            articles[article_id] = {
                "title": title,
                "text": text
            }

        with open(self.cache_path, 'w') as f:
            json.dump(articles, f, indent=2)

        return articles

    def load_articles(self) -> dict:
        if os.path.exists(self.cache_path):
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        return self.parse_and_cache()
