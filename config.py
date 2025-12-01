import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла (если он существует)
# На Render этот файл игнорируется, но на локальной машине он нужен.
load_dotenv()

class Settings:
    # Telegram Bot Token (Ключ: TELEGRAM_BOT_TOKEN)
    BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")

    # Database URL from Render (Ключ: DB_URL)
    DB_URL: str = os.getenv("DB_URL")

    # Ключ для API погоды (Ключ: WEATHER_API_KEY)
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY")

    # Ключ для AI API (Ключ: AI_API_KEY)
    AI_API_KEY: str = os.getenv("AI_API_KEY")

# Создаем объект настроек для использования в других файлах
settings = Settings()
