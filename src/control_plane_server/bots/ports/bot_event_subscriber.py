from typing import Protocol

class BotEventSubscriber(Protocol):
    async def start(self) -> None:
        ...

    async def close(self) -> None:
        ...