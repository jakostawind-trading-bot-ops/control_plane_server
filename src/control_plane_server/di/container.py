from dishka import make_async_container

from control_plane_server.di.shared_providers.nats_client_provider import NatsClientProvider

from control_plane_server.bots.di import(
    NatsBotEventSubscriberProvider,
    NatsBotCommandPublisherProvider,
    BotEventProvider
)

def create_container():
    return make_async_container(
        NatsClientProvider(),
        
        #============================= BOTS MODULE ==============================
        NatsBotCommandPublisherProvider(),
        NatsBotEventSubscriberProvider(),
        BotEventProvider()
        
    )