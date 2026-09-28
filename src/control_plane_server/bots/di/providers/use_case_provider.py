from dishka import Provider, Scope, provide

from control_plane_server.bots.use_cases import *

class BotLifecycleUCProvider(Provider):
    scope = Scope.APP
    
    bot_started_uc = provide(BotStartedUC)