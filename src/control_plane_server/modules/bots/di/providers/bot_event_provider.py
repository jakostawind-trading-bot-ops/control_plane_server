from dishka import Provider, Scope, provide

from control_plane_server.modules.bots.events.dispatcher import BotEventDispatcher
from control_plane_server.modules.bots.transport.nats.bot_event_decoder import BotEventDecoder
from control_plane_server.modules.bots.transport.nats.event_routes.event_routes import BOT_EVENT_ROUTES

from control_plane_server.modules.bots.events import (
    BotStartedEvent, BotStartedHandler
)


class BotEventProvider(Provider):
    scope = Scope.APP
    
    #============================= LIFECYCLE ==============================
    bot_started_handler = provide(BotStartedHandler)

    @provide
    def provide_decoder(self) -> BotEventDecoder:
        return BotEventDecoder(
            routes=BOT_EVENT_ROUTES,
        )
        

    @provide
    def provide_dispatcher(
        self,
        
        #============================= LIFECYCLE ==============================
        bot_started_handler: BotStartedHandler
    ) -> BotEventDispatcher:
        return BotEventDispatcher(
            handlers={
                
                #============================= LIFECYCLE ==============================
                BotStartedEvent: bot_started_handler
            },
        )
