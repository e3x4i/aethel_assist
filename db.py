import asyncpg
from config import settings

# Глобальный пул соединений с базой данных
DB_POOL = None

async def setup_db_pool():
    """Создает пул соединений с PostgreSQL."""
    global DB_POOL
    if settings.DB_URL:
        try:
            DB_POOL = await asyncpg.create_pool(dsn=settings.DB_URL, max_size=10)
            print("Подключение к PostgreSQL успешно установлено.")
        except Exception as e:
            print(f"Ошибка при подключении к БД: {e}")
            DB_POOL = None # Устанавливаем None, чтобы предотвратить дальнейшие ошибки
    else:
        print("ВНИМАНИЕ: Переменная DB_URL не найдена. База данных не будет работать.")

async def close_db_pool():
    """Закрывает пул соединений."""
    global DB_POOL
    if DB_POOL:
        await DB_POOL.close()
        print("Пул соединений с PostgreSQL закрыт.")

async def execute_query(query: str, *args):
    """Выполняет запрос к БД с использованием пула."""
    if not DB_POOL:
        return None # Возвращаем None, если пул не инициализирован

    try:
        # Используем соединение из пула для выполнения запроса
        async with DB_POOL.acquire() as connection:
            # Возвращаем результат выполнения команды (execute, fetchval, fetchrow, fetch)
            return await connection.execute(query, *args)
    except Exception as e:
        print(f"Ошибка выполнения запроса: {e}")
        return None

async def create_tables():
    """Создает необходимые таблицы в базе данных (если они не существуют)."""
    # Таблица для подписок на новости и отслеживания цен
    query = """
    CREATE TABLE IF NOT EXISTS subscriptions (
        user_id BIGINT PRIMARY KEY,
        news_topic VARCHAR(100) DEFAULT 'programming',
        price_url TEXT
    );
    """
    await execute_query(query)
    print("Проверка и создание таблиц завершены.")

# Здесь будут добавляться функции для работы с подписками (добавить/удалить/обновить)
