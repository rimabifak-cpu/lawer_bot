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

from config.settings import settings

# Инициализация логирования
logging.basicConfig(level=logging.INFO)
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

async def main():
    # Импорт хендлеров
    from bot.handlers import register_handlers
    register_handlers(dp)

    # Запускаем HTTP сервер для Render
    await create_http_server()

    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())