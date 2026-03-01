import logging
import queue
import threading
import time
from typing import Dict, Any, List, Callable
from .signal_types import SwarmSignal, SignalType

logger = logging.getLogger(__name__)

class SignalingProtocol:
    """
    DL: Inter-Organism Signaling Protocol.
    Supports Dual-Channel (High/Low priority) communication.
    """
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.high_priority_queue = queue.PriorityQueue()
        self.low_priority_queue = queue.Queue()
        self.handlers: Dict[SignalType, List[Callable[[SwarmSignal], None]]] = {t: [] for t in SignalType}
        self.running = False

    def register_handler(self, signal_type: SignalType, handler: Callable[[SwarmSignal], None]):
        self.handlers[signal_type].append(handler)

    def send_signal(self, signal: SwarmSignal):
        """Simulates sending a signal (broadcast or targeted)"""
        logger.info(f"SWARM_SIGNAL: Agent {self.agent_id} sending {signal.signal_type.name}")
        # In a real swarm, this would go over IPC or Network.
        # Here we simulate delivery by putting it in the local queue if it was for us or broadcast.
        if signal.target_id is None or signal.target_id == self.agent_id:
            self._receive_signal(signal)

    def _receive_signal(self, signal: SwarmSignal):
        if signal.priority > 0:
            self.high_priority_queue.put((-signal.priority, signal))
        else:
            self.low_priority_queue.put(signal)

    def start_listener(self):
        self.running = True
        threading.Thread(target=self._process_queues, daemon=True).start()

    def stop_listener(self):
        self.running = False

    def _process_queues(self):
        while self.running:
            # Process high priority first
            while not self.high_priority_queue.empty():
                _, signal = self.high_priority_queue.get()
                self._dispatch(signal)

            # Then one from low priority to avoid starvation
            try:
                signal = self.low_priority_queue.get(timeout=0.1)
                self._dispatch(signal)
            except queue.Empty:
                # v71.0 Alpha: Functional empty queue handling
                logger.debug("SIGNAL: Queue empty, awaiting signals.")

    def _dispatch(self, signal: SwarmSignal):
        for handler in self.handlers[signal.signal_type]:
            try:
                handler(signal)
            except Exception as e:
                logger.error(f"Error handling signal {signal.signal_type.name}: {e}")
