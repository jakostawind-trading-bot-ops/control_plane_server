from dishka import Provider, Scope, provide

from control_plane_server.modules.bots.use_cases import *

class BotLifecycleUCProvider(Provider):
    scope = Scope.APP
    
    bot_started_uc = provide(BotStartedUC)