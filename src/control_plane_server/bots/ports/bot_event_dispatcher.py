from typing import Protocol

from control_plane_server.bots.events.event import BotEvent


class BotEventDispatcher(Protocol):
    async def dispatch(self, bot_event: BotEvent) -> None:
        ...