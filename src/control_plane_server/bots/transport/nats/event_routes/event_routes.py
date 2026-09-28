from control_plane_server.bots.transport.nats.bot_event_decoder import BotEventRoute
    
from control_plane_server.bots.events import (
    BotStartedEvent
)

from nats_contracts.bot.control.v1 import (
    BotStartedEvMsg
)

BOT_EVENT_ROUTES = {
    # lifecycle
    BotEventRoute(
        msg_type=BotStartedEvMsg.subject_suffix(),
        msg_model=BotStartedEvMsg,
        bot_event_model=BotStartedEvent
    )
}