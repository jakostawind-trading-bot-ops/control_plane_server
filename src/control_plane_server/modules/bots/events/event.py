from dataclasses import dataclass
from abc import abstractmethod, ABC

@dataclass
class BotEvent():
    bot_id: str
    trace_id: str
    payload: dict
    timestamp: str
    
class BotEventHandler(ABC):
    @abstractmethod
    async def handle(self, event: BotEvent):
        ...