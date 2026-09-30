from dishka import make_async_container

from control_plane_server.di.shared_providers.bootstrap_provider import BootstrapProvider
from control_plane_server.di.shared_providers.nats_client_provider import NatsClientProvider

from control_plane_server.modules.bots.di.providers import(
    NatsBotEventSubscriberProvider,
    NatsBotCommandPublisherProvider,
    BotEventProvider,
    BotLifecycleUCProvider
)

def create_container():
    return make_async_container(
        BootstrapProvider(),
        NatsClientProvider(),
        
        #============================= BOTS MODULE ==============================
        NatsBotCommandPublisherProvider(),
        NatsBotEventSubscriberProvider(),
        BotEventProvider(),
        BotLifecycleUCProvider(),
        
        
    )
