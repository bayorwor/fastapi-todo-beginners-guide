# handlers/todo_handler.py
# Handlers hold the actual LOGIC (create, read, update, delete).
# Routes call these functions, so routes stay short and easy to read.
#
# Every function receives "db", a MySQL connection, and runs SQL on the
# "todos" table through a cursor.
#
# ⚠️ Always pass values with %s placeholders, never by building the SQL string
# yourself (e.g. with f-strings). The driver escapes the values safely, which
# protects you from SQL injection.

from typing import List, Optional

from configs.database import Connection
from models.todo import TodoCreate, TodoUpdate


def get_all_todos(db: Connection) -> List[dict]:
    # dictionary=True returns each row as a dict, e.g. {"id": 1, "title": "..."}
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, title, description, completed FROM todos")
    todos = cursor.fetchall()
    cursor.close()
    return todos


def get_todo_by_id(db: Connection, todo_id: int) -> Optional[dict]:
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title, description, completed FROM todos WHERE id = %s",
        (todo_id,),  # the comma makes this a tuple with one value
    )
    todo = cursor.fetchone()  # one row, or None if nothing matched
    cursor.close()
    return todo


def create_todo(db: Connection, data: TodoCreate) -> dict:
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO todos (title, description) VALUES (%s, %s)",
        (data.title, data.description),
    )
    db.commit()                  # save it to MySQL
    new_id = cursor.lastrowid    # the id MySQL generated for the new row
    cursor.close()
    return get_todo_by_id(db, new_id)


def update_todo(db: Connection, todo_id: int, data: TodoUpdate) -> Optional[dict]:
    todo = get_todo_by_id(db, todo_id)
    if todo is None:
        return None

    # Only change the fields the client actually sent; keep the rest as they are
    title = data.title if data.title is not None else todo["title"]
    description = data.description if data.description is not None else todo["description"]
    completed = data.completed if data.completed is not None else todo["completed"]

    cursor = db.cursor()
    cursor.execute(
        "UPDATE todos SET title = %s, description = %s, completed = %s WHERE id = %s",
        (title, description, completed, todo_id),
    )
    db.commit()
    cursor.close()
    return get_todo_by_id(db, todo_id)


def delete_todo(db: Connection, todo_id: int) -> bool:
    cursor = db.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    db.commit()
    deleted = cursor.rowcount > 0  # rowcount = how many rows were deleted
    cursor.close()
    return deleted
