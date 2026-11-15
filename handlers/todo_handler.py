# handlers/todo_handler.py
# Handlers hold the actual LOGIC (create, read, update, delete).
# Routes call these functions, so routes stay short and easy to read.
#
# Every function receives "db", a database session, and uses it to
# read from or write to the "todos" table in MySQL.

from typing import List, Optional

from sqlalchemy.orm import Session

from models.todo import TodoCreate, TodoUpdate
from models.todo_table import TodoTable


def get_all_todos(db: Session) -> List[TodoTable]:
    # SQL: SELECT * FROM todos;
    return db.query(TodoTable).all()


def get_todo_by_id(db: Session, todo_id: int) -> Optional[TodoTable]:
    # SQL: SELECT * FROM todos WHERE id = todo_id LIMIT 1;
    return db.query(TodoTable).filter(TodoTable.id == todo_id).first()


def create_todo(db: Session, data: TodoCreate) -> TodoTable:
    # SQL: INSERT INTO todos (title, description) VALUES (...);
    todo = TodoTable(title=data.title, description=data.description)
    db.add(todo)      # stage the new row
    db.commit()       # save it to MySQL
    db.refresh(todo)  # reload it so we get the id MySQL generated
    return todo


def update_todo(db: Session, todo_id: int, data: TodoUpdate) -> Optional[TodoTable]:
    # SQL: UPDATE todos SET ... WHERE id = todo_id;
    todo = get_todo_by_id(db, todo_id)
    if todo is None:
        return None

    # Only change the fields the client actually sent
    if data.title is not None:
        todo.title = data.title
    if data.description is not None:
        todo.description = data.description
    if data.completed is not None:
        todo.completed = data.completed

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int) -> bool:
    # SQL: DELETE FROM todos WHERE id = todo_id;
    todo = get_todo_by_id(db, todo_id)
    if todo is None:
        return False
    db.delete(todo)
    db.commit()
    return True
