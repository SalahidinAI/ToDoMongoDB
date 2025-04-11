from datetime import datetime
from typing import List, Optional
from enum import Enum
from beanie import Link, Document, Indexed


class StatusChoices(str, Enum):
    to_do = 'to_do'
    in_progress = 'in_progress'
    done = 'done'
    expired = 'expired'


class User(Document):
    email: str
    first_name: str
    username: Indexed(str, unique=True)
    password: str
    created_date: datetime = datetime.utcnow()
    user_tasks: Optional[List[Link['Task']]] = None

    class Settings:
        name = 'user'


class Task(Document):
    user: Optional[Link[User]] = None
    title: str
    description: str
    deadline: datetime
    status: StatusChoices = StatusChoices.to_do
    created_date: datetime = datetime.utcnow()

    class Settings:
        name = 'task'
