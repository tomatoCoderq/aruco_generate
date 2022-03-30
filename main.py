from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.generate_marker import register_handlers_generate
from app.handlers.common import register_handlers_common

import sqlite3, logging, asyncio
logger = logging.getLogger(__name__)



async def main():
    logging.basicConfig(
        level = logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    config = load_config('config/conf.ini')

    bot = Bot(token = config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_generate(dp)
    register_handlers_common(dp)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())