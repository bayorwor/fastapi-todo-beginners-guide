# models/todo.py
# Models describe the SHAPE of the data our API receives and sends back.
# FastAPI uses them (via Pydantic) to validate requests automatically.

from typing import Optional

from pydantic import BaseModel


class TodoCreate(BaseModel):
    """Data the client sends when CREATING a todo."""
    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    """Data the client sends when UPDATING a todo. Every field is optional,
    so the client only sends what it wants to change."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    """A full todo item, as the API returns it."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
