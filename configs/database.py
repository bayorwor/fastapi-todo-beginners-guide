# configs/database.py
# Everything needed to talk to the MySQL database lives here.
#
#   engine       -> the connection to MySQL
#   SessionLocal -> creates a "session" (a conversation with the database)
#   Base         -> the parent class for all our table models
#   get_db()     -> gives each request its own session, then closes it

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

from configs.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# Build the connection address, e.g. mysql+pymysql://root:@127.0.0.1:3306/todo_db
# URL.create safely handles special characters (like @ or #) in the password.
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",  # MySQL, using the PyMySQL driver
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# pool_pre_ping checks the connection is still alive before using it
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    """Open a database session for one request, and always close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
