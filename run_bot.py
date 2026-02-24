import asyncio
import logging
import sys
import os
from aiohttp import web

# Добавляем директорию проекта в путь Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.exceptions import TelegramUnauthorizedError

from config.settings import settings

# Инициализация логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# HTTP сервер для Render (чтобы детектировал открытый порт)
async def health_handler(request):
    return web.json_response({"status": "ok"})

async def create_http_server():
    app = web.Application()
    app.router.add_get('/health', health_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get('PORT', 8080)))
    await site.start()
    logger.info(f"HTTP server started on port {os.environ.get('PORT', 8080)}")
    return runner

async def check_bot_token():
    """Проверка токена бота"""
    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot token valid. Bot: @{bot_info.username} (ID: {bot_info.id})")
        return True
    except TelegramUnauthorizedError:
        logger.error("Invalid bot token! Check BOT_TOKEN environment variable.")
        return False
    except Exception as e:
        logger.error(f"Error checking bot token: {e}")
        return False

async def main():
    # Импорт хендлеров
    from bot.handlers import register_handlers
    register_handlers(dp)

    # Проверка переменных окружения
    logger.info(f"BOT_TOKEN set: {'Yes' if settings.BOT_TOKEN else 'No'}")
    logger.info(f"DATABASE_URL set: {'Yes' if os.environ.get('DATABASE_URL') else 'No'}")
    logger.info(f"PORT: {os.environ.get('PORT', 'Not set')}")

    # Проверка токена бота
    token_valid = await check_bot_token()
    if not token_valid:
        logger.error("Bot token invalid. Exiting...")
        return

    # Запускаем HTTP сервер для Render
    await create_http_server()

    logger.info("Starting bot polling...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Polling error: {e}")

if __name__ == "__main__":
    asyncio.run(main())