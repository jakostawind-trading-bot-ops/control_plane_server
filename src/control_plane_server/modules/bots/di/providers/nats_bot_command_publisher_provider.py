import logging

import nats
from dishka import Provider, Scope, provide
from nats.aio.client import Client
from nats.js.client import JetStreamContext

from nats_contracts.control.bot.v1.common.subjects import CONTROL_TO_BOT_COMMANDS_JETSTEAM

from control_plane_server.modules.bots.ports.bot_command_publisher import BotCommandPublisher
from control_plane_server.modules.bots.transport.nats.bot_command_publisher import NatsBotCommandPublisher

logger = logging.getLogger(__name__)

class NatsBotCommandPublisherProvider(Provider):
    scope = Scope.APP
    
    @provide
    def provide_jetstream(
        self,
        nats_client: Client,
    ) -> JetStreamContext:
        return nats_client.jetstream()
    
    @provide
    def provide_nats_publisher(
        self,
        jetstream: JetStreamContext,
    ) -> BotCommandPublisher:
        return NatsBotCommandPublisher(
            jetstream = jetstream,
            stream_name = CONTROL_TO_BOT_COMMANDS_JETSTEAM
        )