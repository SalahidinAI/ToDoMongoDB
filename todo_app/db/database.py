from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import User, Task
from todo_app.config import config


client = AsyncIOMotorClient(
        config.MONGODB_URL
)
database = client[config.DB_NAME]


async def init_db():
    await init_beanie(database=database, document_models=[User, Task])
