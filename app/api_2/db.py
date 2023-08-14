from motor.motor_asyncio import AsyncIOMotorClient
from app.core.settings import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.MONGODB_NAME]

collection_brands = database["brands"]
