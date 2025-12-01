import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from config import settings
# from db import setup_db_pool, close_db_pool, create_tables  # ЗАКОММЕНТИРОВАНО

# --- Настройка логирования ---
logging.basicConfig(level=logging.INFO)

# --- Инициализация бота ---
if not settings.BOT_TOKEN:
    logging.error("Токен бота не найден. Установите переменную TELEGRAM_BOT_TOKEN.")
    # Вместо выхода (exit) лучше вернуть исключение, чтобы Scalingo увидел ошибку
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in environment variables.")

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# --- Обработчики команд ---

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    """Ответ на команду /start."""
    await message.answer(
        f"Привет, **{message.from_user.full_name}**! Я твой многофункциональный ассистент."
        f"\n\nИспользуй команды:"
        f"\n/weather [Город] - получить погоду."
        f"\n/news - настроить подписку на новости."
        f"\n/price [URL] - отслеживать цену товара."
        f"\n/generate [Текст] - создать изображение.",
        parse_mode="Markdown"
    )

@dp.message(Command("weather"))
async def command_weather_handler(message: types.Message):
    """Заглушка для модуля погоды."""
    # TODO: Реализовать логику запроса к OpenWeatherMap через aiohttp
    if settings.WEATHER_API_KEY:
        await message.answer("🛠️ Модуль погоды в разработке. (Используй aiohttp и OpenWeatherMap API).")
    else:
         await message.answer("⚠️ Ключ WEATHER_API_KEY не установлен. Модуль недоступен.")


@dp.message(Command("news"))
async def command_news_handler(message: types.Message):
    """Заглушка для модуля новостей."""
    # TODO: Реализовать логику работы с БД (db.py) для сохранения подписки пользователя.
    await message.answer("📰 Модуль новостей в разработке. (Требуется подключение к БД).")

@dp.message(Command("price"))
async def command_price_handler(message: types.Message):
    """Заглушка для модуля отслеживания цен."""
    # TODO: Реализовать логику Web Scraping (BeautifulSoup) и сохранения URL/цены в БД.
    await message.answer("💰 Модуль отслеживания цен в разработке. (Требуется подключение к БД).")

@dp.message(Command("generate"))
async def command_generate_handler(message: types.Message):
    """Заглушка для модуля генерации контента."""
    # TODO: Реализовать логику запроса к AI API через aiohttp
    if settings.AI_API_KEY:
        await message.answer("🎨 Модуль генерации контента в разработке. (Используй aiohttp и AI API).")
    else:
        await message.answer("⚠️ Ключ AI_API_KEY не установлен. Модуль недоступен.")


# --- Главная функция запуска ---
async def main():
    # 1. Настройка базы данных - ВРЕМЕННО ЗАКОММЕНТИРОВАНО
    # await setup_db_pool()
    
    # if settings.DB_URL:
        # 2. Создание таблиц - ВРЕМЕННО ЗАКОММЕНТИРОВАНО
        # await create_tables()

    # 3. Запуск бота (Long Polling)
    # Этот вызов блокирует процесс и держит Worker запущенным 24/7
    await dp.start_polling(bot)

    # 4. Закрытие соединения с БД - ВРЕМЕННО ЗАКОММЕНТИРОВАНО
    # await close_db_pool()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # Ловим ошибку, если токен не установлен
        logging.error(f"Критическая ошибка: {e}")
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем.")
    except Exception as e:
        # Обработка других исключений при запуске
        logging.error(f"Бот остановлен из-за критической ошибки: {e}")
