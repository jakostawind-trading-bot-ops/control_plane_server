import logging

logger = logging.getLogger(__name__)

class BotStartedUC():
    async def execute(self):
        logger.info("сработал execute BotStartedUC")