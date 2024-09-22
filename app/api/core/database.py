from motor.motor_asyncio import AsyncIOMotorClient
from app.api.core.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.mongodb_db]

async def initialize_database():
    await db.customers.create_index("email_address", unique=True)
