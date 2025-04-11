from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import User, Task

async def init_db():
    client = AsyncIOMotorClient(
        'mongodb+srv://Salahidin:012456789Salahmon@cluster0.rxmbdp2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    )
    database = client['ToDo']
    await init_beanie(database=database, document_models=[User, Task])
