import logging
from collections.abc import AsyncIterator

import nats
from dishka import Provider, Scope, provide
from nats.aio.client import Client
from nats.js.client import JetStreamContext


from control_plane_server.bots.events.dispatcher import BotEventDispatcher
from control_plane_server.bots.transport.nats.bot_event_decoder import BotEventDecoder
from control_plane_server.bots.ports.bot_event_subscriber import BotEventSubscriber
from control_plane_server.bots.transport.nats.bot_event_subscriber import NatsBotEventSubscriber

logger = logging.getLogger(__name__)

class NatsBotEventSubscriberProvider(Provider):
    scope = Scope.APP
    
    @provide
    async def provide_nats_bot_event_subscriber(
        self,
        jetstream: JetStreamContext,
        decoder: BotEventDecoder,
        dispatcher: BotEventDispatcher,
    ) -> AsyncIterator[BotEventSubscriber]:
        subscriber = NatsBotEventSubscriber(
            jetstream=jetstream,
            stream_name="BOT_TO_CONTROL_EVENTS",
            subject_prefix=(
                f"bot.*.to.control.event."
            ),
            consumer_name=(
                f"control_plane_server_bots"
            ),
            decoder=decoder,
            dispatcher=dispatcher,
        )
        
        await subscriber.start()

        try:
            yield subscriber
        finally:
            await subscriber.close()
    