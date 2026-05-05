from typing import Any, Dict, Optional

class ProvenanceTracker:
    @staticmethod
    def attach_pipeline(asset: Any, pipeline: str) -> Any:
        """
        Attaches pipeline provenance metadata to an asset.
        """
        if hasattr(asset, 'metadata'):
            asset.metadata['pipeline'] = pipeline
        elif isinstance(asset, dict):
            asset['pipeline'] = pipeline
        return asset

    @staticmethod
    def get_pipeline(asset: Any) -> Optional[str]:
        """
        Retrieves the pipeline provenance from an asset.
        """
        if hasattr(asset, 'metadata'):
            return asset.metadata.get('pipeline')
        elif isinstance(asset, dict):
            return asset.get('pipeline')
        return None
