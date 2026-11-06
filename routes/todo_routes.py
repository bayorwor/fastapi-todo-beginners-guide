# routes/todo_routes.py
# Routes define the URLs (endpoints) of our API and which HTTP method each uses.
# Each route receives the request, calls a handler, and returns the result.

from typing import List

from fastapi import APIRouter, HTTPException

from constant.messages import TODO_DELETED, TODO_NOT_FOUND
from handlers import todo_handler
from models.todo import Todo, TodoCreate, TodoUpdate

# Every route in this file will start with /todos
router = APIRouter(prefix="/todos", tags=["Todos"])


# GET /todos  -> list all todos
@router.get("/", response_model=List[Todo])
def list_todos():
    return todo_handler.get_all_todos()


# GET /todos/1  -> get one todo by its id
@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = todo_handler.get_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


# POST /todos  -> create a new todo (201 = "Created")
@router.post("/", response_model=Todo, status_code=201)
def create_todo(data: TodoCreate):
    return todo_handler.create_todo(data)


# PUT /todos/1  -> update an existing todo
@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, data: TodoUpdate):
    todo = todo_handler.update_todo(todo_id, data)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


# DELETE /todos/1  -> delete a todo
@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    if not todo_handler.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return {"message": TODO_DELETED}
