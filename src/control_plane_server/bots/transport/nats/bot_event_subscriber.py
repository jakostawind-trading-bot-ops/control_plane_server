import logging

from nats.aio.msg import Msg
from nats.js.client import JetStreamContext

from control_plane_server.bots.events.dispatcher import BotEventDispatcher
from control_plane_server.bots.transport.nats.bot_event_decoder import BotEventDecoder, BotEventDecodeError

logger = logging.getLogger(__name__)


class NatsBotEventSubscriber:
    def __init__(
        self,
        jetstream: JetStreamContext,
        stream_name: str,
        subject_prefix: str,
        consumer_name: str,
        decoder: BotEventDecoder,
        dispatcher: BotEventDispatcher,
    ) -> None:
        self._jetstream = jetstream
        self._stream_name = stream_name
        self._subject_prefix = subject_prefix
        self._consumer_name = consumer_name
        self._decoder = decoder
        self._dispatcher = dispatcher
        self._subscription = None

    async def start(self) -> None:
        subject = f"{self._subject_prefix}>"
        logger.info(
            "Запуск NATS subscriber команд "
            "stream=%s consumer=%s subject=%s",
            self._stream_name,
            self._consumer_name,
            subject,
        )

        self._subscription = await self._jetstream.subscribe(
            subject=subject,
            durable=self._consumer_name,
            stream=self._stream_name,
            cb=self._handle_message,
            manual_ack=True,
        )

        logger.info(
            "NATS subscriber команд запущен consumer=%s",
            self._consumer_name,
        )

    async def close(self) -> None:
        if self._subscription is None:
            logger.debug(
                "NATS subscriber команд уже остановлен "
                "consumer=%s",
                self._consumer_name,
            )
            return

        logger.info(
            "Остановка NATS subscriber команд consumer=%s",
            self._consumer_name,
        )

        await self._subscription.unsubscribe()
        self._subscription = None

        logger.info(
            "NATS subscriber команд остановлен consumer=%s",
            self._consumer_name,
        )

    async def _handle_message(self, message: Msg) -> None:
        logger.debug(
            "Получена команда из NATS subject=%s size_bytes=%d",
            message.subject,
            len(message.data),
        )

        try:
            message_type = self._extract_message_type(
                message.subject,
            )

            bot_event = self._decoder.decode(
                msg_type=message_type,
                raw_message=message.data,
            )

            logger.info(
                "Команда декодирована bot_event=%s trace_id=%s subject=%s",
                type(bot_event).__name__,
                bot_event.trace_id,
                message.subject,
            )
        except BotEventDecodeError as error:
            logger.warning(
                "Некорректная команда в subject %s: %s",
                message.subject,
                error,
            )
            await message.term()
            logger.debug(
                "Доставка некорректной команды прекращена subject=%s",
                message.subject,
            )
            return
        except Exception:
            logger.exception(
                "Не удалось декодировать команду в subject %s",
                message.subject,
            )
            await message.term()
            logger.debug(
                "Доставка команды прекращена из-за ошибки subject=%s",
                message.subject,
            )
            return

        try:
            await self._dispatcher.dispatch(bot_event)
        except Exception as error:
            logger.exception(
                "Ошибка обработки ивента bot_event=%s trace_id=%s subject=%s",
                type(bot_event).__name__,
                bot_event.trace_id,
                message.subject,
            )
            await message.term() #todo: испрвить этот момент
            return

        logger.info(
            "Команда обработана bot_event=%s trace_id=%s",
            type(bot_event).__name__,
            bot_event.trace_id,
        )

        await message.ack()
        logger.debug(
            "Для команды отправлен ACK bot_event=%s trace_id=%s",
            type(bot_event).__name__,
            bot_event.trace_id,
        )

    def _extract_message_type(self, subject: str) -> str:
        prefix_parts = self._subject_prefix.removesuffix(".").split(".")
        subject_parts = subject.split(".")

        if len(subject_parts) <= len(prefix_parts) or any(
            expected != "*" and expected != actual
            for expected, actual in zip(prefix_parts, subject_parts)
        ):
            raise BotEventDecodeError(
                f"Unexpected subject: {subject}"
            )

        message_type = ".".join(subject_parts[len(prefix_parts):])

        if not message_type:
            raise BotEventDecodeError("Missing bot_event type")

        return message_type
