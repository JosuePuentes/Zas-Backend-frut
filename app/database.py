"""Conexión a MongoDB usando Motor (async)."""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

settings = get_settings()
client: AsyncIOMotorClient | None = None
db = None


async def connect_to_mongo():
    """Conectar a MongoDB."""
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db_name]


async def close_mongo_connection():
    """Cerrar conexión a MongoDB."""
    global client
    if client:
        client.close()


def get_database():
    """Obtener instancia de la base de datos."""
    return db
