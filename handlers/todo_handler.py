# handlers/todo_handler.py
# Handlers hold the actual LOGIC (create, read, update, delete).
# Routes call these functions, so routes stay short and easy to read.
#
# We store todos in a Python list (in memory). This is fine for learning,
# but the data is lost every time the server restarts. Later you can swap
# this for a real database without changing the routes.

from typing import List, Optional

from models.todo import Todo, TodoCreate, TodoUpdate

todos: List[Todo] = []  # our "database"
next_id = 1             # used to give each new todo a unique id


def get_all_todos() -> List[Todo]:
    return todos


def get_todo_by_id(todo_id: int) -> Optional[Todo]:
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None  # not found


def create_todo(data: TodoCreate) -> Todo:
    global next_id
    todo = Todo(id=next_id, title=data.title, description=data.description)
    todos.append(todo)
    next_id += 1
    return todo


def update_todo(todo_id: int, data: TodoUpdate) -> Optional[Todo]:
    todo = get_todo_by_id(todo_id)
    if todo is None:
        return None

    # Only change the fields the client actually sent
    if data.title is not None:
        todo.title = data.title
    if data.description is not None:
        todo.description = data.description
    if data.completed is not None:
        todo.completed = data.completed
    return todo


def delete_todo(todo_id: int) -> bool:
    todo = get_todo_by_id(todo_id)
    if todo is None:
        return False
    todos.remove(todo)
    return True
