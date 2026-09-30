from dishka import Provider, Scope, provide

from control_plane_server.bootstrap_settings import (
    BootstrapSettings,
    load_bootstrap_settings,
)


class BootstrapProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_bootstrap_settings(self) -> BootstrapSettings:
        return load_bootstrap_settings()
