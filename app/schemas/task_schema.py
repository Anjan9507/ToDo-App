from enum import Enum
from pydantic import BaseModel
from datetime import date

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: date

class TaskCreateResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: date


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    overdue = "overdue"

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: TaskStatus
    due_date: date

class TaskUpdateResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    due_date: date

