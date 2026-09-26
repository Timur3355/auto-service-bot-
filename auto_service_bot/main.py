import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN
from database import init_db
from handlers import start_router, catalog_router, calculator_router, booking_router

# НАСТРОЙКИ ПРОКСИ (замени на свои данные, если есть)
# Если прокси нет, оставь proxy_url = None
PROXY_URL = None 
# Пример: "socks5://user:pass@127.0.0.1:1080" или "http://127.0.0.1:8080"

async def main():
    await init_db()
    
    # Создаем сессию с прокси (если он указан)
    session = AiohttpSession()
    if PROXY_URL:
        from aiohttp_socks import ProxyConnector
        connector = ProxyConnector.from_url(PROXY_URL)
        session.connector = connector

    bot = Bot(
        token=BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session # Передаем нашу сессию
    )
    
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(calculator_router)
    dp.include_router(booking_router)
    dp.include_router(catalog_router)
    
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())