from typing import Protocol

from control_plane_server.modules.bots.commands.control_command import ControlCommand

class BotCommandPublisher(Protocol):
    async def publish_command(self, control_command: ControlCommand):
        ...