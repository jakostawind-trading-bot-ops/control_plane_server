import logging

from control_plane_server.bots.events.event import BotEvent, BotEventHandler


logger = logging.getLogger(__name__)


class BotEventDispatcher:
    def __init__(
        self,
        handlers: dict[type[BotEvent], BotEventHandler],
    ) -> None:
        self._handlers = handlers

    async def dispatch(self, bot_event: BotEvent) -> None:
        handler = self._handlers.get(type(bot_event))

        if handler is None:
            raise RuntimeError(type(bot_event))

        logger.debug(
            "Передача ивента в handler bot_event=%s handler=%s trace_id=%s",
            type(bot_event).__name__,
            type(bot_event).__name__,
            bot_event.trace_id,
        )

        await handler.handle(bot_event)

        logger.debug(
            "Dispatch ивента завершён bot_event=%s trace_id=%s",
            type(bot_event).__name__,
            bot_event.trace_id,
        )
