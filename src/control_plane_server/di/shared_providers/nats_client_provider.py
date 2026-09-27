import logging
from collections.abc import AsyncIterator

import nats
from dishka import Provider, Scope, provide
from nats.aio.client import Client

logger = logging.getLogger(__name__)

class NatsClientProvider(Provider):
    scope = Scope.APP
    
    @provide
    async def provide_nats_client(
        self,
    ) -> AsyncIterator[Client]:
        logger.info("Подключение к NATS")

        try:
            client = await nats.connect(
                servers = ["nats://127.0.0.1:4222"],
                user = "control_plane_server",
                password = "control_plane_server_password"
            )
        except Exception:
            logger.exception("Не удалось подключиться к NATS")
            raise

        logger.info("Соединение с NATS установлено")

        try:
            yield client
        finally:
            logger.info("Закрытие соединения с NATS")
            await client.close()
            logger.info("Соединение с NATS закрыто")