from dishka import Provider, Scope, provide

from control_plane_server.bots.events.dispatcher import BotEventDispatcher
from control_plane_server.bots.transport.nats.bot_event_decoder import BotEventDecoder


class BotEventProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_decoder(self) -> BotEventDecoder:
        return BotEventDecoder(
            routes=(),
        )

    @provide
    def provide_dispatcher(self) -> BotEventDispatcher:
        return BotEventDispatcher(
            handlers={},
        )
