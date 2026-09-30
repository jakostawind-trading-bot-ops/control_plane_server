import json
from collections.abc import Iterable
from dataclasses import dataclass
from pydantic import ValidationError

from nats_contracts.bot.control.v1 import BotMessage

from control_plane_server.modules.bots.events.event import BotEvent


class BotEventDecodeError(ValueError):
    """Полученная команда не соответствует контракту."""


@dataclass(frozen=True, slots=True)
class BotEventRoute:
    msg_type: str # суффикс NATS сабджект для поиска ивента. Например "lifecycle.RunBotEvent"
    msg_model: type[BotMessage] # класс модели из nats_contracts
    bot_event_model: type[BotEvent] # внутренняя команда бота


class BotEventDecoder:
    def __init__(
        self,
        routes: Iterable[BotEventRoute],
    ) -> None:
        self._routes: dict[str, BotEventRoute] = {}

        for route in routes:
            if route.msg_type in self._routes:
                raise RuntimeError(
                    f"Duplicate BotEvent route: {route.msg_type}"
                )

            self._routes[route.msg_type] = route

    def decode(
        self,
        msg_type: str,
        raw_message: bytes,
    ) -> BotEvent:

        route = self._routes.get(msg_type)

        if route is None:
            raise BotEventDecodeError(
                f"Unsupported BotEvent type: {msg_type}"
            )

        try:
            message = route.msg_model.model_validate_json(
                raw_message
            )
        except ValidationError as error:
            raise BotEventDecodeError(
                f"Invalid mmessage contract: {msg_type}"
            ) from error
            
        try:
            return route.bot_event_model(
                bot_id=message.bot_id,
                trace_id=message.message.trace_id,
                payload=message.payload.model_dump(),
                timestamp=message.timestamp,
            )
        except TypeError as error:
            raise RuntimeError(
                f"Message payload does not match BotEvent {msg_type}"
            ) from error
