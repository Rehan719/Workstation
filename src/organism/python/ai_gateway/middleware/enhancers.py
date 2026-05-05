import functools
import logging
from src.organism.python.ai_gateway import gateway

logger = logging.getLogger(__name__)

def ai_ingestion_enhancer(provider: str = "deepseek"):
    """
    Evolutionary Decorator to wrap existing ingestors with DeepSeek/AI enhancements.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. Execute legacy ingestion first
            legacy_results = await func(*args, **kwargs)

            logger.info(f"AIInhancer: Enhancing legacy results with {provider}...")

            # 2. AI-driven meta-analysis of extracted content
            # (In a real scenario, we'd pass the actual content)
            prompt = [
                {"role": "system", "content": "Analyze the following extracted evidence for UK Employment Tribunal relevance."},
                {"role": "user", "content": f"Summary of ingested data: {str(legacy_results)[:1000]}"}
            ]

            try:
                ai_meta = await gateway.execute_completion(provider, prompt)

                # 3. Merge AI insights into results
                if isinstance(legacy_results, list):
                    for item in legacy_results:
                        item["ai_forensic_analysis"] = ai_meta["content"]
                elif isinstance(legacy_results, dict):
                    legacy_results["ai_forensic_analysis"] = ai_meta["content"]

            except Exception as e:
                logger.error(f"AIEnhancer: AI augmentation failed, returning legacy data only. {e}")

            return legacy_results
        return wrapper
    return decorator
