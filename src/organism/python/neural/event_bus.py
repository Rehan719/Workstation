import asyncio
import logging
import collections
import time
from typing import Dict, Any, List, Callable, Type, Optional
from .event_types import BiomimeticEvent

logger = logging.getLogger(__name__)

class Subscription:
    def __init__(self, event_type: Type, handler: Callable):
        self.event_type = event_type
        self.handler = handler

class AsyncEventBus:
    """
    Asynchronous event bus with priority queueing and backpressure handling.
    """
    def __init__(self, max_queue_size: int = 1000):
        self._subscriptions: Dict[Type, List[Callable]] = collections.defaultdict(list)
        self._queue = asyncio.PriorityQueue(maxsize=max_queue_size)
        self._is_running = False
        self._worker_task: Optional[asyncio.Task] = None
        self._history: collections.deque = collections.deque(maxlen=100)
        self._dead_letter_queue: List[Dict[str, Any]] = []

    async def start(self):
        """Starts the event processing loop."""
        if not self._is_running:
            self._is_running = True
            self._worker_task = asyncio.create_task(self._worker())
            logger.info("AsyncEventBus: Neural Bus processing started.")

    async def stop(self):
        """Stops the event processing loop."""
        self._is_running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            self._worker_task = None
            logger.info("AsyncEventBus: Neural Bus processing stopped.")

    async def _worker(self):
        while self._is_running:
            try:
                priority, timestamp, event = await self._queue.get()
                await self._dispatch(event)
                self._queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"AsyncEventBus: Worker loop error: {e}")
                await asyncio.sleep(0.1)

    async def _dispatch(self, event: BiomimeticEvent):
        """Dispatches an event to all interested subscribers."""
        event_type = type(event)
        handlers = list(self._subscriptions.get(event_type, []))

        if event_type != BiomimeticEvent:
            handlers.extend(self._subscriptions.get(BiomimeticEvent, []))

        tasks = []
        for handler in handlers:
            tasks.append(self._handle_safe(handler, event))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _handle_safe(self, handler: Callable, event: BiomimeticEvent):
        """Runs a handler safely and logs failures."""
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)
        except Exception as e:
            logger.error(f"AsyncEventBus: Handler failure for event {event.id}: {e}")
            self._dead_letter_queue.append({
                "event": event,
                "handler": handler.__name__ if hasattr(handler, "__name__") else str(handler),
                "error": str(e),
                "timestamp": time.time()
            })

    async def publish(self, event: BiomimeticEvent):
        """Publishes an event to the bus."""
        try:
            await self._queue.put((event.priority, time.time(), event))
            self._history.append(event)
        except asyncio.QueueFull:
            logger.warning(f"AsyncEventBus: Queue full! Dropping event {event.id}")

    def subscribe(self, event_type: Type, handler: Callable) -> Subscription:
        """Registers a handler for a specific event type."""
        self._subscriptions[event_type].append(handler)
        logger.debug(f"AsyncEventBus: Handler registered for {event_type.__name__}")
        return Subscription(event_type, handler)

    def unsubscribe(self, subscription: Subscription):
        """Unregisters a specific subscription."""
        if subscription.event_type in self._subscriptions:
            if subscription.handler in self._subscriptions[subscription.event_type]:
                self._subscriptions[subscription.event_type].remove(subscription.handler)
                logger.debug(f"AsyncEventBus: Handler unregistered for {subscription.event_type.__name__}")

    def get_history(self) -> List[BiomimeticEvent]:
        """Returns the recent event history."""
        return list(self._history)

    def get_dlq(self) -> List[Dict[str, Any]]:
        """Returns the Dead Letter Queue."""
        return self._dead_letter_queue
