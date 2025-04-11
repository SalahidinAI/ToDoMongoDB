from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from .models import StatusChoices


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    username: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    username: Optional[str] = None
    password: str


class UserGet(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    username: str
    password: str
    created_date: datetime


class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: datetime


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    status: Optional[StatusChoices] = None


class TaskGet(BaseModel):
    id: str
    title: str
    description: str
    deadline: datetime
    status: StatusChoices
    created_date: datetime
    user: Optional[int] = None
