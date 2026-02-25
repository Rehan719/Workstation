import logging
import time

logger = logging.getLogger(__name__)

class CircadianScheduler:
    """
    Multi-oscillator scheduler: Ultradian, Circadian, Infradian.
    """
    def __init__(self):
        self.start_time = time.time()

    def get_current_cycle(self) -> str:
        elapsed = time.time() - self.start_time

        # Ultradian (90-120 min) - Work/Rest
        ultradian_elapsed = elapsed % (120 * 60)
        if ultradian_elapsed < (90 * 60):
            mode = "FOCUS"
        else:
            mode = "REST"

        # Circadian (24h) - Maintenance
        circadian_elapsed = elapsed % (24 * 3600)
        if (22 * 3600) < circadian_elapsed or circadian_elapsed < (2 * 3600):
            return f"MAINTENANCE_{mode}"

        return f"ACTIVE_{mode}"

    def schedule_task(self, task_name: str, resource_intensity: float):
        cycle = self.get_current_cycle()
        logger.info(f"CIRCADIAN: Scheduling {task_name} during {cycle} phase.")
        if "MAINTENANCE" in cycle and resource_intensity > 0.7:
             logger.info("CIRCADIAN: Optimal window for high-intensity maintenance.")
        elif "REST" in cycle:
             logger.info("CIRCADIAN: Low power mode - delaying intensive tasks.")
