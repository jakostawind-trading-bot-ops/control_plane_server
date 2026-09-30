import logging
from dataclasses import asdict

from nats.js.client import JetStreamContext

from nats_contracts.control.bot.v1 import ControlMessage
from nats_contracts.control.bot.v1.common.subjects import generate_control_to_bot_command_subject

from control_plane_server.modules.bots.commands.control_command import ControlCommand
from control_plane_server.modules.bots.transport.nats.command_contracts.registry import COMMAND_CONTRACTS

logger = logging.getLogger(__name__)

class NatsBotCommandPublisher():
    def __init__(
            self,
            jetstream: JetStreamContext,
            stream_name: str,
        ) -> None:
            self.jetstream = jetstream
            self.stream_name = stream_name
        
    @staticmethod
    def build_payload(control_command: ControlCommand):
        excluded = {"message_id", "trace_id", "timestamp"}
        
        return {
            name: value for name, value in asdict(control_command).items()
            if name not in excluded
        }
    
    def encode_command(
        self,
        control_command: ControlCommand
    ) -> tuple[str, ControlMessage]:
        logger.debug(
            "Кодирование event event=%s message_id=%s trace_id=%s",
            type(control_command).__name__,
            control_command.message_id,
            control_command.trace_id,
        )

        contract_type = COMMAND_CONTRACTS.get(type(control_command))
        
        if contract_type is None:
            raise RuntimeError(f"Ивент неподдерживается: {type(control_command).__name__}")
        
        message = contract_type(
            bot_id="test_bot",
            message={
                "message_id": str(control_command.message_id),
                "trace_id": str(control_command.trace_id),
            },
            payload=self.build_payload(control_command),
            timestamp=control_command.timestamp
        )
        
        subject = generate_control_to_bot_command_subject(
            bot_id="test_bot",
            subject_suffix=contract_type.subject_suffix(),
        )

        logger.debug(
            "Event закодирован event=%s subject=%s",
            type(control_command).__name__,
            subject,
        )

        return subject, message
    
    async def publish_command(self, control_command: ControlCommand):
        try:
            subject, message = self.encode_command(control_command)

            logger.info(
                "Публикация event event=%s message_id=%s "
                "trace_id=%s stream=%s subject=%s",
                type(control_command).__name__,
                control_command.message_id,
                control_command.trace_id,
                self.stream_name,
                subject,
            )

            await self.jetstream.publish_async(
                subject=subject,
                payload=message.model_dump_json().encode("utf-8"),
                stream=self.stream_name,
            )
        except Exception:
            logger.exception(
                "Ошибка публикации event=%s message_id=%s stream=%s subject=%s",
                type(control_command).__name__,
                control_command.message_id,
                self.stream_name,
                subject,
            )
            raise

        logger.info(
            "Event опубликован event=%s message_id=%s subject=%s",
            type(control_command).__name__,
            control_command.message_id,
            subject,
        )