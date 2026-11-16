# models/todo_table.py
# This file describes the "todos" TABLE in MySQL, written as plain SQL.
# configs/database.py runs it when the app starts.
#
# Don't confuse it with models/todo.py:
#   todo_table.py -> what is stored in the DATABASE (SQL table)
#   todo.py       -> what the API receives and sends (Pydantic)

# "IF NOT EXISTS" means: create the table only if it isn't there yet,
# so restarting the app never deletes your data.
CREATE_TODOS_TABLE = """
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- MySQL picks the next number for us
    title VARCHAR(255) NOT NULL,            -- required, max 255 characters
    description TEXT NULL,                  -- optional, long text allowed
    completed BOOLEAN NOT NULL DEFAULT FALSE
)
"""
