# models/todo_table.py
# This model describes the "todos" TABLE in MySQL (built with SQLAlchemy).
# Each class attribute becomes a column in the table.
#
# Don't confuse it with models/todo.py:
#   todo_table.py -> what is stored in the DATABASE (SQLAlchemy)
#   todo.py       -> what the API receives and sends (Pydantic)

from sqlalchemy import Boolean, Column, Integer, String, Text

from configs.database import Base


class TodoTable(Base):
    __tablename__ = "todos"  # the table name in MySQL

    id = Column(Integer, primary_key=True, index=True)  # MySQL auto-increments this
    title = Column(String(255), nullable=False)          # required, max 255 characters
    description = Column(Text, nullable=True)            # optional, long text allowed
    completed = Column(Boolean, default=False, nullable=False)
