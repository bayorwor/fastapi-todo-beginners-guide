# configs/database.py
# Everything needed to talk to the MySQL database lives here.
# We use the official MySQL driver, mysql-connector-python, and write plain SQL.
#
#   get_connection() -> opens a new connection to MySQL
#   get_db()         -> gives each request its own connection, then closes it
#   create_tables()  -> creates our tables when the app starts (if missing)

import mysql.connector
# "Connection" is a short name for "a MySQL connection", used in type hints across the app
from mysql.connector.abstracts import MySQLConnectionAbstract as Connection

from configs.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from models.todo_table import CREATE_TODOS_TABLE


def get_connection() -> Connection:
    """Open a new connection to the MySQL database."""
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def get_db():
    """Open a database connection for one request, and always close it afterwards."""
    db = get_connection()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create any missing tables (existing tables and their data are left alone)."""
    db = get_connection()
    try:
        cursor = db.cursor()
        cursor.execute(CREATE_TODOS_TABLE)
        cursor.close()
    finally:
        db.close()
