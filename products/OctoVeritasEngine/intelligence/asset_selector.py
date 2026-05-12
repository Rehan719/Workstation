from typing import List, Optional

class FormatSelector:
    def __init__(self, effectiveness_engine: Any):
        self.effectiveness_engine = effectiveness_engine

    def select_best_format(self,
                           content_type: str,
                           mode: str,
                           audience: str,
                           device: str = "desktop") -> str:
        # Integrated with Truth V (Predictive) and Truth IX (Learning)
        # For now, delegates to effectiveness engine or returns mode default
        try:
            prediction = self.effectiveness_engine.predict_format(content_type, audience, device)
            if prediction:
                return prediction
        except Exception as e:
            print(f"Error predicting asset format: {e}")
        return "HTML"

class AssetSelector:
    def filter_redundant(self, assets: List[Any], mode: str) -> List[Any]:
        # Logic to skip detailed assets if summary exists (unless in Mushahida)
        if mode == "mushahida":
            return assets

        # Simple heuristic: prioritize summary/knowledge over raw scraping
        has_summary = any(a.get('pipeline') in ['Knowledge', 'Learning'] for a in assets)
        if has_summary:
            return [a for a in assets if a.get('pipeline') != 'Scraping']
        return assets
