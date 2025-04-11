from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from todo_app.db.database import init_db
from todo_app.api import users, tasks

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

todo_app = FastAPI(title='ToDo Site', lifespan=lifespan)

todo_app.include_router(users.user_router)
todo_app.include_router(tasks.task_router)

if __name__ == '__main__':
    uvicorn.run(todo_app, host='127.0.0.1', port=9000)
