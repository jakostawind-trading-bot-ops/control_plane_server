from dataclasses import dataclass
import logging

from control_plane_server.modules.bots.events.event import BotEvent, BotEventHandler
from control_plane_server.modules.bots.use_cases import BotStartedUC

logger = logging.getLogger(__name__)

@dataclass
class BotStartedEvent(BotEvent):
    ...
    
class BotStartedHandler(BotEventHandler):
    def __init__(
        self,
        bot_started_uc: BotStartedUC
    ):
        self.bot_started_uc = bot_started_uc
        
    async def handle(
        self, 
        event: BotStartedEvent
    ):
        logger.info("Сработал хендлер BotStartedEvent")
        await self.bot_started_uc.execute()