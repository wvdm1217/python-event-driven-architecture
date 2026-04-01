import asyncio
from typing import Any, Callable, ClassVar, Dict, List, Type, Union
from pydantic import BaseModel

class Event(BaseModel):
    """Base class for all events. Enforces a routing topic."""
    __topic__: ClassVar[str]

class EventFramework:
    def __init__(self):
        self.queues: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[str, List[Callable]] = {}
        self._tasks: List[asyncio.Task] = []

    def subscribe(self, event_model: Type[Event]):
        """Decorator to register a worker to an event's topic."""
        def decorator(func: Callable):
            topic = event_model.__topic__
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            
            self.subscribers[topic].append(func)
            return func
        return decorator

    async def publish(self, event: Event):
        """Pushes an event onto its designated topic queue."""
        topic = event.__topic__
        if topic not in self.queues:
            self.queues[topic] = asyncio.Queue()
        
        print(f"[Broker] Publishing to '{topic}': {event}")
        await self.queues[topic].put(event)

    async def _handle_worker_result(self, result: Any):
        """Inspects worker returns and auto-publishes outgoing events."""
        if result is None:
            return
        
        if isinstance(result, Event):
            await self.publish(result)
        elif isinstance(result, (list, tuple)):
            for item in result:
                if isinstance(item, Event):
                    await self.publish(item)

    async def _consume(self, topic: str):
        """Background loop that pulls events from a queue and runs workers."""
        queue = self.queues[topic]
        while True:
            event = await queue.get()
            
            for worker_func in self.subscribers.get(topic, []):
                try:
                    result = await worker_func(event)
                    await self._handle_worker_result(result)
                except Exception as e:
                    print(f"[Error] Worker failed on topic '{topic}': {e}")
            
            queue.task_done()

    async def start(self):
        """Starts the consumer loops for all registered topics."""
        for topic in self.subscribers.keys():
            if topic not in self.queues:
                self.queues[topic] = asyncio.Queue()
            
            task = asyncio.create_task(self._consume(topic))
            self._tasks.append(task)
        
        print("[System] Framework started and listening to queues...")

    async def stop(self):
        """Cancels all background consumer tasks."""
        for task in self._tasks:
            task.cancel()
        print("[System] Framework stopped.")