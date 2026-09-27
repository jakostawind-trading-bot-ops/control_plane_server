import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from control_plane_server.logging_config import configure_logging, shutdown_logging

from control_plane_server.di.container import create_container
from control_plane_server.bots.ports.bot_event_subscriber import BotEventSubscriber

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    try:
        async with create_container() as container:
            await container.get(BotEventSubscriber)
            yield
    finally:
        shutdown_logging()


app = FastAPI(lifespan=lifespan)