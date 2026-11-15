# Todo API with FastAPI: A Beginner's Tutorial

This project is a small **Todo API** built with [FastAPI](https://fastapi.tiangolo.com/), a Python framework for building backend APIs.

You can use it in two ways:

1. **Run it** and play with a working API in your browser.
2. **Rebuild it yourself**, step by step, by following the tutorial below. It comes in two parts:
   - **[Part 1](#part-1-build-the-api-step-by-step)**: build the API and keep todos in a Python list (in memory).
   - **[Part 2](#part-2-connect-to-a-mysql-database)**: connect it to a **MySQL database** (using Laragon, XAMPP, WAMP or Herd), so your todos are saved permanently.

> The code in this repository is the **finished Part 2 version**, so it uses MySQL.

By the end you will know how to:

- Set up a Python project with a virtual environment
- Organise a FastAPI project into clear folders
- Describe your data with Pydantic models
- Build the 5 basic API operations: **Create, Read, Update, Delete** (CRUD)
- Return proper errors (like `404 Not Found`)
- Keep settings and passwords in a `.env` file
- Connect to a MySQL database and save data with SQLAlchemy
- Test your API with the interactive docs FastAPI builds for you

---

## Table of Contents

- [What is an API?](#what-is-an-api)
- [Prerequisites](#prerequisites)
- [Quick Start (run the finished project)](#quick-start-run-the-finished-project)
- [Project Structure](#project-structure)
- [Packages Used](#packages-used)
- [How a Request Flows](#how-a-request-flows)
- [Environment Variables (.env)](#environment-variables-env)
- [The Endpoints](#the-endpoints)
- [Part 1: Build the API, Step by Step](#part-1-build-the-api-step-by-step)
- [Part 2: Connect to a MySQL Database](#part-2-connect-to-a-mysql-database)
- [Testing Your API](#testing-your-api)
- [Key Concepts Cheat Sheet](#key-concepts-cheat-sheet)
- [Common Errors and Fixes](#common-errors-and-fixes)
- [Exercises: Build Something Similar](#exercises-build-something-similar)
- [Next Steps](#next-steps)

---

## What is an API?

An **API** (Application Programming Interface) lets one program talk to another. A **web API** works over HTTP, the same way your browser talks to websites.

A client (a website, a mobile app or another program) sends a **request** to a **URL** using an **HTTP method**. The server sends back a **response**, usually as **JSON**.

| HTTP Method | Meaning | Example in this project |
|---|---|---|
| `GET` | Read data | Get all todos |
| `POST` | Create new data | Add a new todo |
| `PUT` | Update existing data | Mark a todo as completed |
| `DELETE` | Remove data | Delete a todo |

Each response also carries a **status code** that says how the request went:

| Code | Meaning |
|---|---|
| `200` | OK, it worked |
| `201` | Created, a new item was made |
| `404` | Not Found, the item doesn't exist |
| `422` | Unprocessable, the data you sent is invalid |

---

## Prerequisites

- **Python 3.8 or newer**. Check your version with:
  ```bash
  python --version
  ```
- A code editor. [VS Code](https://code.visualstudio.com/) is recommended.
- Basic Python knowledge: variables, functions, lists, `if` statements and classes.
- **For Part 2 and the Quick Start:** a local MySQL server. The easiest way to get one is a bundle such as [Laragon](https://laragon.org/), [XAMPP](https://www.apachefriends.org/), [WampServer](https://www.wampserver.com/) or [Laravel Herd](https://herd.laravel.com/). Setup for each is explained in [Part 2, Step 1](#step-1-install-and-start-mysql).

---

## Quick Start (run the finished project)

**1. Open a terminal in the project folder** (`todo-app`).

**2. Create and activate a virtual environment.** A virtual environment keeps this project's packages separate from the rest of your computer.

```bash
# Create it (only needed once)
python -m venv venv

# Activate it on Windows (PowerShell)
venv\Scripts\activate

# Activate it on macOS / Linux
source venv/bin/activate
```

When it is active, you will see `(venv)` at the start of your terminal line.

**3. Install the packages:**

```bash
pip install -r requirements.txt
```

This installs every package listed in `requirements.txt`. To find out what each one does, see [Packages Used](#packages-used).

**4. Create your `.env` file** by copying the template:

```bash
# Windows (PowerShell)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

The defaults work for Laragon, XAMPP and WAMP (user `root`, no password). If your MySQL uses a different password or port, change `DB_PASSWORD` or `DB_PORT` in `.env`. See [Environment Variables](#environment-variables-env) for more.

**5. Start MySQL and create the database.** Start MySQL in Laragon, XAMPP, WAMP or Herd, then create an empty database called `todo_db`. [Part 2, Steps 1 and 2](#step-1-install-and-start-mysql) show how. You don't need to create any tables: the app creates them when it starts.

**6. Start the server:**

```bash
uvicorn main:app --reload
```

- `main` is the file `main.py`
- `app` is the `FastAPI()` object inside that file
- `--reload` restarts the server every time you save a file

**7. Open the interactive docs** at **http://127.0.0.1:8000/docs**

You will see every endpoint listed. Click one, press **Try it out**, then **Execute**. 🎉

To stop the server, press `Ctrl + C` in the terminal.

---

## Project Structure

```
todo-app/
├── main.py                  # Entry point: creates the app and connects the routes
├── requirements.txt         # The packages this project needs
├── .env                     # YOUR local settings (not committed to Git)
├── .env.example             # Template showing which settings are needed (committed)
├── .gitignore               # Files Git should ignore (venv, __pycache__, .env, ...)
├── configs/
│   ├── __init__.py
│   ├── settings.py          # Loads app settings from .env
│   └── database.py          # Connects to MySQL (Part 2)
├── constant/
│   ├── __init__.py
│   └── messages.py          # Reusable text, e.g. "Todo not found"
├── models/
│   ├── __init__.py
│   ├── todo.py              # The SHAPE of the API's data (Pydantic)
│   └── todo_table.py        # The "todos" TABLE in MySQL (SQLAlchemy, Part 2)
├── handlers/
│   ├── __init__.py
│   └── todo_handler.py      # The LOGIC: create, read, update, delete (in MySQL)
└── routes/
    ├── __init__.py
    └── todo_routes.py       # The URLs (endpoints) of the API
```

### Why split the code into folders?

You *could* put everything in `main.py`. That works for tiny projects, but it gets messy quickly. Giving each folder **one job** makes the code easier to read, test and grow.

| Folder | Job | Real-world comparison |
|---|---|---|
| `routes/` | Receives requests and sends responses | The **waiter** taking your order |
| `models/` | Defines and validates the data | The **menu**: what you're allowed to order |
| `handlers/` | Does the actual work | The **kitchen** cooking the food |
| `constant/` | Stores fixed values used in many places | The restaurant's **standard phrases** |
| `configs/` | Loads settings and connects to the database | The restaurant's **name, opening hours and supplier contacts** |
| MySQL database | Stores the data permanently | The **pantry** where food is kept |

> **What is `__init__.py`?** It is an empty file that tells Python "this folder is a package", so you can import from it, e.g. `from models.todo import Todo`.

---

## Packages Used

A **package** is code someone else wrote and shared, so you don't have to build everything yourself. Python packages are installed with `pip` from [PyPI](https://pypi.org/), the Python Package Index.

This project's packages are listed in `requirements.txt`:

```text
fastapi
uvicorn[standard]
python-dotenv
sqlalchemy
pymysql
cryptography
```

### At a glance

| Package | Job in one sentence | Used in | Needed for |
|---|---|---|---|
| `fastapi` | The web framework that turns Python functions into API endpoints | `main.py`, `routes/` | Part 1 |
| `uvicorn[standard]` | The server that runs the app and listens for requests | the terminal (`uvicorn main:app`) | Part 1 |
| `python-dotenv` | Reads settings from the `.env` file | `configs/settings.py` | Part 1 |
| `sqlalchemy` | Lets you work with database tables using Python classes | `configs/database.py`, `models/todo_table.py`, `handlers/` | Part 2 |
| `pymysql` | The driver that carries messages between Python and MySQL | `configs/database.py`, through the `mysql+pymysql` URL | Part 2 |
| `cryptography` | Handles the secure login that MySQL 8 requires | used by `pymysql` behind the scenes | Part 2 |

### `fastapi`

**What it is:** the framework this whole project is built on. A *framework* gives you a structure and ready-made tools, so you only write the parts that are specific to your app.

**What it does for us:**
- Connects URLs to Python functions (`@router.get("/")`)
- Reads path parameters and JSON bodies and converts them to the right Python types
- Validates incoming data and returns a `422` error when it's wrong
- Turns our return values into JSON
- Builds the interactive `/docs` and `/redoc` pages automatically

**Where you see it:**

```python
from fastapi import APIRouter, Depends, FastAPI, HTTPException
```

**It brings two important packages with it** (installed automatically, so they're not in `requirements.txt`):

| Package | What it does |
|---|---|
| **Pydantic** | Data validation. Our `TodoCreate`, `TodoUpdate` and `Todo` classes in `models/todo.py` are Pydantic models (`from pydantic import BaseModel`) |
| **Starlette** | The lower-level web toolkit FastAPI is built on top of. You rarely use it directly |

📖 Docs: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

### `uvicorn[standard]`

**What it is:** an **ASGI server**. FastAPI *describes* how to answer requests, but it can't listen on a network port by itself. Uvicorn is the program that actually runs, waits for requests on `http://127.0.0.1:8000`, and hands them to FastAPI.

> 🍽️ Restaurant comparison: FastAPI is the menu and the kitchen's recipes. Uvicorn is the front door that lets customers in.

**Where you see it:** only in the terminal.

```bash
uvicorn main:app --reload
```

**What does `[standard]` mean?** The square brackets install **extras**: optional add-ons that make Uvicorn faster and more capable. They include `watchfiles`, which powers `--reload`, and faster networking libraries. Plain `pip install uvicorn` works too, but `[standard]` is recommended.

> In PowerShell or zsh, wrap it in quotes so the brackets aren't misread: `pip install "uvicorn[standard]"`.

📖 Docs: [uvicorn.org](https://www.uvicorn.org/)

### `python-dotenv`

**What it is:** a small package that reads a `.env` file and loads each line (`NAME=value`) as an **environment variable**.

**Why we need it:** Python can already read environment variables with `os.getenv(...)`, but it doesn't know about `.env` files. `python-dotenv` fills that gap, so settings and passwords stay out of the code.

**Where you see it:** `configs/settings.py`

```python
from dotenv import load_dotenv

load_dotenv()                     # reads .env
APP_NAME = os.getenv("APP_NAME")  # now available through os.getenv
```

> ⚠️ The package is called **`python-dotenv`**, but you import it as **`dotenv`**. `pip install dotenv` installs a *different* package, so double-check the name.

📖 Docs: [pypi.org/project/python-dotenv](https://pypi.org/project/python-dotenv/)

### `sqlalchemy`

**What it is:** an **ORM** (Object Relational Mapper) and database toolkit. It lets you describe tables as Python classes and work with rows as Python objects, instead of writing SQL by hand.

**Without SQLAlchemy** (raw SQL):

```python
cursor.execute("INSERT INTO todos (title) VALUES (%s)", ("Buy milk",))
```

**With SQLAlchemy:**

```python
db.add(TodoTable(title="Buy milk"))
db.commit()
```

**What it does for us:**
- Defines the `todos` table (`class TodoTable(Base)`)
- Creates the table when the app starts (`Base.metadata.create_all`)
- Manages connections (`create_engine`) and sessions (`sessionmaker`)
- Writes the SQL for `SELECT`, `INSERT`, `UPDATE` and `DELETE`

A bonus: SQLAlchemy works with many databases (MySQL, PostgreSQL, SQLite, ...). To switch, you mostly change the connection URL and driver, not your handler code.

**Where you see it:** `configs/database.py`, `models/todo_table.py`, `handlers/todo_handler.py` and `routes/todo_routes.py` (for the `Session` type).

📖 Docs: [docs.sqlalchemy.org](https://docs.sqlalchemy.org/en/20/)

### `pymysql`

**What it is:** a MySQL **driver**, written in pure Python. SQLAlchemy knows *what* SQL to send, but it needs a driver to actually *talk* to a specific database. PyMySQL speaks MySQL's network language.

> 📞 Comparison: SQLAlchemy decides what to say, PyMySQL is the phone line to MySQL.

**Where you see it:** you never import it yourself. SQLAlchemy loads it because of the connection URL in `configs/database.py`:

```python
drivername="mysql+pymysql"   # database = mysql, driver = pymysql
```

It works with MySQL **and** MariaDB, so it suits all four tools in Part 2 (Laragon, XAMPP, WAMP and Herd).

📖 Docs: [pymysql.readthedocs.io](https://pymysql.readthedocs.io/)

### `cryptography`

**What it is:** a library for encryption and other security tasks.

**Why we need it:** MySQL 8 logs users in with a secure method called `caching_sha2_password`. PyMySQL needs `cryptography` to handle it. Without it, connecting fails with:

```text
RuntimeError: 'cryptography' package is required for sha256_password or caching_sha2_password auth methods
```

**Where you see it:** nowhere in our code. PyMySQL uses it behind the scenes.

> Some setups (like XAMPP's MariaDB with an empty password) may connect without it. Keep it installed anyway, so the project works on every machine.

📖 Docs: [cryptography.io](https://cryptography.io/)

### Working with `requirements.txt`

| Task | Command |
|---|---|
| Install everything listed | `pip install -r requirements.txt` |
| Install a new package | `pip install package-name`, then add its name to `requirements.txt` |
| See what's installed | `pip list` |
| See a package's details | `pip show fastapi` |
| Save exact versions of everything installed | `pip freeze > requirements.txt` |

**Pinned vs. unpinned versions:**

| Style | Example | Meaning |
|---|---|---|
| Unpinned (this project) | `fastapi` | Install the latest version. Simple, but a future release could change behaviour |
| Pinned | `fastapi==0.162.0` | Install exactly this version. Everyone gets the same setup |

`pip freeze` writes pinned versions of **every** installed package, including ones that came along automatically (like Pydantic). That's normal.

> ⚠️ Only Python packages belong in `requirements.txt`. JavaScript libraries (like `axios`) are installed with `npm` and listed in `package.json` instead. Putting them here makes `pip install -r requirements.txt` fail.

---

## How a Request Flows

Here is what happens when a client sends `POST /todos/` with `{"title": "Buy milk"}`:

```
   Client (browser / app)
          │   POST /todos/   {"title": "Buy milk"}
          ▼
   ┌───────────────┐
   │   main.py     │  FastAPI app receives the request
   └──────┬────────┘
          ▼
   ┌───────────────┐
   │   routes/     │  Finds the matching endpoint: create_todo()
   └──────┬────────┘
          ▼
   ┌───────────────┐
   │   models/     │  Checks the data: is "title" a string? ✔
   └──────┬────────┘
          ▼
   ┌───────────────┐
   │   handlers/   │  Creates the todo and asks the database to save it
   └──────┬────────┘
          ▼
   ┌───────────────┐
   │    MySQL      │  INSERT INTO todos ... (MySQL gives it id = 1)
   └──────┬────────┘
          ▼
   Response: 201 Created
   {"id": 1, "title": "Buy milk", "description": null, "completed": false}
```

---

## Environment Variables (`.env`)

Settings like the app name or a database password should **not** be written directly in your code. They go in a `.env` file instead:

```env
APP_NAME=Todo API
APP_VERSION=1.0.0
APP_DESCRIPTION=A simple Todo API built with FastAPI for learning.

# MySQL connection (Laragon / XAMPP / WAMP default: user "root" with an empty password)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=todo_db
```

| Setting | Meaning |
|---|---|
| `DB_HOST` | The computer MySQL runs on. `127.0.0.1` means "this computer" |
| `DB_PORT` | The "door number" MySQL listens on. Usually `3306` |
| `DB_USER` / `DB_PASSWORD` | The MySQL login |
| `DB_NAME` | The database that holds our tables |

**Why?**

- **Security:** `.env` is listed in `.gitignore`, so secrets never get pushed to GitHub.
- **Flexibility:** each computer (your laptop, a teammate's, a server) can have different values without changing any code.

**The two files:**

| File | Committed to Git? | Purpose |
|---|---|---|
| `.env` | ❌ No | Your real, local values |
| `.env.example` | ✅ Yes | A template so others know which settings to create |

**How the app reads them:** [configs/settings.py](configs/settings.py) uses the `python-dotenv` package. `load_dotenv()` reads `.env`, and `os.getenv("NAME", default)` gets each value. If a value is missing, the default is used.

> ⚠️ After changing `.env`, **restart the server**. `--reload` only watches `.py` files.

**Adding a new setting:**

1. Add it to `.env`, e.g. `DEBUG=true`
2. Add it to `.env.example` too, so others know about it
3. Read it in `configs/settings.py`: `DEBUG = os.getenv("DEBUG", "false") == "true"`
4. Import it where you need it: `from configs.settings import DEBUG`

> 💡 Every value read from `.env` is a **string**. Convert it yourself when you need a number or boolean, e.g. `int(os.getenv("PORT", "8000"))`.

---

## The Endpoints

| Method | URL | Description | Request body | Success response |
|---|---|---|---|---|
| `GET` | `/` | Welcome message | none | `200` |
| `GET` | `/todos/` | List all todos | none | `200` + list of todos |
| `GET` | `/todos/{todo_id}` | Get one todo | none | `200` + the todo |
| `POST` | `/todos/` | Create a todo | `{"title": "...", "description": "..."}` | `201` + the new todo |
| `PUT` | `/todos/{todo_id}` | Update a todo | Any of `title`, `description`, `completed` | `200` + the updated todo |
| `DELETE` | `/todos/{todo_id}` | Delete a todo | none | `200` + success message |

If a todo doesn't exist, the endpoints that take a `{todo_id}` return:

```json
{ "detail": "Todo not found" }
```

with status code `404`.

---

## Part 1: Build the API, Step by Step

Follow these steps in a **new, empty folder** to recreate the project from scratch. Type the code yourself rather than copying it. You will learn much more that way.

In Part 1 the todos live in a Python list, so you can focus on FastAPI without setting up a database. [Part 2](#part-2-connect-to-a-mysql-database) swaps the list for MySQL.

### Step 1: Set up the project

```bash
mkdir my-todo-api
cd my-todo-api

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install fastapi "uvicorn[standard]" python-dotenv
```

Save the installed packages so others can install them later:

```bash
pip freeze > requirements.txt
```

Create a `.gitignore` file so Git skips files that shouldn't be shared:

```gitignore
venv/
__pycache__/
.env
```

### Step 2: Create the folders

Create these five folders, each with an **empty** `__init__.py` file inside:

```
configs/__init__.py
constant/__init__.py
models/__init__.py
handlers/__init__.py
routes/__init__.py
```

### Step 3: Settings (`.env` + `configs/settings.py`)

First, create a `.env` file in the project root with your settings:

```env
APP_NAME=Todo API
APP_VERSION=1.0.0
APP_DESCRIPTION=A simple Todo API built with FastAPI for learning.
```

Copy it to `.env.example` as well. That copy gets committed so others know which settings they need.

Then load the settings in `configs/settings.py`, so the rest of the app imports them from one place:

```python
import os

from dotenv import load_dotenv

load_dotenv()  # reads the .env file and adds its values to the environment

APP_NAME = os.getenv("APP_NAME", "Todo API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "A simple Todo API built with FastAPI for learning.")
```

The second argument of `os.getenv` is a **default**, used when the value is missing from `.env`.

### Step 4: Constants (`constant/messages.py`)

Text that is used in more than one place goes here. If you want to change a message, you change it once.

```python
TODO_NOT_FOUND = "Todo not found"
TODO_DELETED = "Todo deleted successfully"
```

### Step 5: Models (`models/todo.py`)

Models describe **what our data looks like**. They are built with **Pydantic**, which comes with FastAPI. FastAPI uses them to:

- **Validate** incoming data. Sending `"title": 123` or leaving out `title` gives an automatic `422` error.
- **Document** your API on the `/docs` page.

```python
from typing import Optional

from pydantic import BaseModel


class TodoCreate(BaseModel):
    """Data the client sends when CREATING a todo."""
    title: str                          # required
    description: Optional[str] = None   # optional (defaults to None)


class TodoUpdate(BaseModel):
    """Data the client sends when UPDATING a todo.
    Every field is optional, so the client only sends what it wants to change."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    """A full todo item, as the API returns it."""
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
```

> 💡 **Why three models?** Each one fits a different situation:
> - When **creating**, the client should not choose the `id`. The server does that.
> - When **updating**, the client may only want to change one field.
> - When **responding**, we send back everything.

### Step 6: Handlers (`handlers/todo_handler.py`)

Handlers contain the **logic**. They don't know anything about URLs or HTTP. They only work with data.

To keep things simple we store todos in a **Python list** instead of a database.

```python
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
```

> ⚠️ **The data disappears when the server restarts.** The list only lives in memory. That's fine for learning. In [Part 2](#part-2-connect-to-a-mysql-database) we fix this by saving todos in MySQL.

### Step 7: Routes (`routes/todo_routes.py`)

Routes connect **URLs + HTTP methods** to handler functions.

```python
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
```

**Understanding the pieces:**

| Code | What it means |
|---|---|
| `APIRouter(prefix="/todos")` | A group of related routes, all starting with `/todos` |
| `tags=["Todos"]` | Groups these endpoints under a "Todos" heading on the `/docs` page |
| `@router.get("/")` | "When someone sends a GET request to `/todos/`, run the function below" |
| `"/{todo_id}"` | A **path parameter**: the value in the URL (e.g. `/todos/5`) is passed into the function as `todo_id` |
| `todo_id: int` | FastAPI converts the value to an `int` and rejects values like `/todos/abc` |
| `data: TodoCreate` | FastAPI reads the **JSON body** of the request and validates it against the model |
| `response_model=Todo` | Tells FastAPI what shape the response has (filters it and documents it) |
| `raise HTTPException(404, ...)` | Stops the function and sends an error response to the client |

### Step 8: The entry point (`main.py`)

Finally, create the app and plug in the router.

```python
from fastapi import FastAPI

from configs.settings import APP_DESCRIPTION, APP_NAME, APP_VERSION
from routes.todo_routes import router as todo_router

app = FastAPI(title=APP_NAME, version=APP_VERSION, description=APP_DESCRIPTION)

# Register the todo routes with the app
app.include_router(todo_router)


@app.get("/")
def home():
    return {"message": f"Welcome to the {APP_NAME}! Visit /docs to try the API."}
```

### Step 9: Run it 🚀

```bash
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs**. Congratulations, you built a REST API!

Now create a few todos, stop the server (`Ctrl + C`) and start it again. Your todos are gone. Part 2 fixes that.

---

## Part 2: Connect to a MySQL Database

In this part we replace the Python list with a real **MySQL database**, so todos are saved permanently.

### A few words first

| Term | Meaning |
|---|---|
| **Database server** | A program (MySQL) that stores data and keeps running in the background |
| **Database** | A named container inside the server, e.g. `todo_db` |
| **Table** | Like a spreadsheet inside the database, e.g. `todos`, with **columns** (`id`, `title`, ...) and **rows** (one per todo) |
| **SQL** | The language used to talk to databases, e.g. `SELECT * FROM todos;` |
| **ORM** | Object Relational Mapper. It lets you work with tables using **Python classes** instead of writing SQL. We use **SQLAlchemy**, the most popular Python ORM |
| **Driver** | The package that actually carries messages between Python and MySQL. We use **PyMySQL** |

**What changes compared to Part 1?**

| File | Change |
|---|---|
| `.env` / `configs/settings.py` | Add the database login settings |
| `configs/database.py` | **New:** connects to MySQL |
| `models/todo_table.py` | **New:** describes the `todos` table |
| `models/todo.py` | One small addition so Pydantic can read database rows |
| `handlers/todo_handler.py` | Use the database instead of the list |
| `routes/todo_routes.py` | Give each request a database session |
| `main.py` | Create the table when the app starts |

### Step 1: Install and start MySQL

Pick **one** of the tools below. They all give you the same thing: a MySQL server running on your computer.

> ⚠️ **Only run one at a time.** Each one starts MySQL on port `3306`, and two programs can't use the same port. If you have Laragon *and* XAMPP installed, stop MySQL in one before starting the other.

#### Option A: Laragon (recommended for Windows)

1. Download and install Laragon from [laragon.org](https://laragon.org/download/).
2. Open Laragon and click **Start All**.
3. When the **MySQL** row turns green, MySQL is running on port `3306`.
4. Click **Database** to open **HeidiSQL**, a visual database tool. Log in with user `root` and an **empty** password.

#### Option B: XAMPP

1. Download and install XAMPP from [apachefriends.org](https://www.apachefriends.org/).
2. Open the **XAMPP Control Panel**.
3. Click **Start** next to **MySQL**. Also start **Apache** if you want to use phpMyAdmin.
4. Open **http://localhost/phpmyadmin** in your browser to manage your databases.

> XAMPP actually ships **MariaDB**, a close relative of MySQL. It works with this project without any changes.

#### Option C: WampServer (WAMP)

1. Download and install WampServer from [wampserver.com](https://www.wampserver.com/en/).
2. Start WampServer and wait until the tray icon turns **green**.
3. Open **http://localhost/phpmyadmin** and log in with user `root` and an empty password.

> ⚠️ WAMP often runs **MariaDB on port `3306`** and **MySQL on port `3308`**. Check the port in the tray menu: left-click the icon, then **MySQL** → **my.ini** or **Use a port other than 3306**. Set `DB_PORT` in `.env` to match.

#### Option D: Laravel Herd

1. Download and install Herd from [herd.laravel.com](https://herd.laravel.com/).
2. Open Herd → **Services** → add a **MySQL** service and start it.
3. Check the **port**, **user** and **password** shown in the service settings, and copy them into your `.env`.
4. Herd has no built-in database screen, so use a free tool such as [HeidiSQL](https://www.heidisql.com/), [TablePlus](https://tableplus.com/) or [MySQL Workbench](https://www.mysql.com/products/workbench/).

> Database services are part of **Herd Pro**, the paid version. With the free version, use one of the other options.

#### Default logins at a glance

| Tool | Host | Port | User | Password | Database tool |
|---|---|---|---|---|---|
| Laragon | `127.0.0.1` | `3306` | `root` | *(empty)* | HeidiSQL (**Database** button) |
| XAMPP | `127.0.0.1` | `3306` | `root` | *(empty)* | phpMyAdmin (`/phpmyadmin`) |
| WAMP | `127.0.0.1` | `3306` or `3308` | `root` | *(empty)* | phpMyAdmin (`/phpmyadmin`) |
| Herd | `127.0.0.1` | see Herd's service settings | see Herd | see Herd | HeidiSQL / TablePlus |

### Step 2: Create the database

Our app creates the **table** by itself, but the **database** must exist first. Choose one way:

**Using a visual tool:**
- **HeidiSQL (Laragon):** right-click the connection on the left → **Create new** → **Database** → name it `todo_db` → **OK**.
- **phpMyAdmin (XAMPP / WAMP):** click **New** in the left sidebar → type `todo_db` → **Create**.

**Using SQL:** open the SQL/query tab of any of these tools and run:

```sql
CREATE DATABASE todo_db;
```

**Using the terminal (Laragon):** click **Terminal** in Laragon, then run:

```bash
mysql -u root -e "CREATE DATABASE todo_db;"
```

### Step 3: Install the Python packages

With your virtual environment active:

```bash
pip install sqlalchemy pymysql cryptography
pip freeze > requirements.txt
```

| Package | What it does |
|---|---|
| `sqlalchemy` | The ORM: lets us use Python classes instead of SQL |
| `pymysql` | The driver that connects Python to MySQL |
| `cryptography` | Needed by PyMySQL to log in to MySQL 8, which uses a secure login method |

### Step 4: Add the database settings

Add these lines to **both** `.env` and `.env.example`:

```env
# MySQL connection (Laragon / XAMPP / WAMP default: user "root" with an empty password)
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=todo_db
```

> 🔒 If you set a real password, put it only in `.env`, **never** in `.env.example`.

Then read them at the bottom of `configs/settings.py`:

```python
# Database settings
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))  # .env values are strings, so convert to int
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "todo_db")
```

### Step 5: Connect to MySQL (`configs/database.py`)

Create a new file, `configs/database.py`. This is the only file that knows *how* to connect to MySQL.

```python
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
```

**Understanding the pieces:**

| Code | What it means |
|---|---|
| `DATABASE_URL` | The "address" of the database: which driver, login, host, port and database name |
| `engine` | The actual connection to MySQL, created once and shared by the whole app |
| `SessionLocal` | A factory that makes **sessions**. A session is one "conversation" with the database |
| `Base` | The parent class every table model inherits from |
| `get_db()` | Opens a session for a request and **always closes it** afterwards, even if an error happens. `yield` hands the session to the route and waits until the request is done |

### Step 6: Describe the table (`models/todo_table.py`)

Create a new file, `models/todo_table.py`. Each class attribute becomes a **column** in the `todos` table.

```python
from sqlalchemy import Boolean, Column, Integer, String, Text

from configs.database import Base


class TodoTable(Base):
    __tablename__ = "todos"  # the table name in MySQL

    id = Column(Integer, primary_key=True, index=True)  # MySQL auto-increments this
    title = Column(String(255), nullable=False)          # required, max 255 characters
    description = Column(Text, nullable=True)            # optional, long text allowed
    completed = Column(Boolean, default=False, nullable=False)
```

> 💡 **Two kinds of model, two jobs.** It's easy to mix these up:
>
> | File | Library | Describes |
> |---|---|---|
> | `models/todo.py` | Pydantic | What the **API** receives and sends (JSON) |
> | `models/todo_table.py` | SQLAlchemy | What is stored in the **database** (table and columns) |

### Step 7: Let Pydantic read database rows (`models/todo.py`)

Our handlers will now return `TodoTable` objects instead of Pydantic `Todo` objects. To let FastAPI turn them into JSON, add **one line** to the `Todo` class and update the import:

```python
from pydantic import BaseModel, ConfigDict

# ... TodoCreate and TodoUpdate stay the same ...


class Todo(BaseModel):
    """A full todo item, as the API returns it."""
    # Lets Pydantic read data straight from a database row (a TodoTable object)
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
```

### Step 8: Use the database in the handlers (`handlers/todo_handler.py`)

Replace the whole file. Each function now receives `db`, a database session. The comments show the SQL that SQLAlchemy writes for you.

```python
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
```

Notice that the `todos` list and the `next_id` counter are gone. MySQL now stores the todos and generates the ids.

**The session methods you'll use most:**

| Method | What it does |
|---|---|
| `db.query(TodoTable).all()` | Get every row |
| `db.query(TodoTable).filter(...).first()` | Get the first row that matches, or `None` |
| `db.add(obj)` | Mark a new object to be saved |
| `db.commit()` | **Save all changes** to the database. Nothing is saved until you commit! |
| `db.refresh(obj)` | Reload the object from the database (e.g. to get its new `id`) |
| `db.delete(obj)` | Mark a row to be deleted (saved on `commit`) |

### Step 9: Give each request a session (`routes/todo_routes.py`)

Every route gets a new argument, `db: Session = Depends(get_db)`, and passes `db` to the handler. Here is the full file:

```python
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from configs.database import get_db
from constant.messages import TODO_DELETED, TODO_NOT_FOUND
from handlers import todo_handler
from models.todo import Todo, TodoCreate, TodoUpdate

# Every route in this file will start with /todos
router = APIRouter(prefix="/todos", tags=["Todos"])

# "db: Session = Depends(get_db)" asks FastAPI to open a database session
# for each request and pass it in. FastAPI closes it when the request ends.


# GET /todos  -> list all todos
@router.get("/", response_model=List[Todo])
def list_todos(db: Session = Depends(get_db)):
    return todo_handler.get_all_todos(db)


# GET /todos/1  -> get one todo by its id
@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_handler.get_todo_by_id(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


# POST /todos  -> create a new todo (201 = "Created")
@router.post("/", response_model=Todo, status_code=201)
def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    return todo_handler.create_todo(db, data)


# PUT /todos/1  -> update an existing todo
@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, data: TodoUpdate, db: Session = Depends(get_db)):
    todo = todo_handler.update_todo(db, todo_id, data)
    if todo is None:
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return todo


# DELETE /todos/1  -> delete a todo
@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    if not todo_handler.delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail=TODO_NOT_FOUND)
    return {"message": TODO_DELETED}
```

> 💡 **What is `Depends`?** It's FastAPI's **dependency injection**. Instead of opening and closing a database session inside every route, you tell FastAPI "this route *depends on* `get_db`". FastAPI then calls `get_db()` for you, passes the session in, and cleans up afterwards.

### Step 10: Create the table on startup (`main.py`)

Add three lines to `main.py`:

```python
from fastapi import FastAPI

from configs.database import Base, engine
from configs.settings import APP_DESCRIPTION, APP_NAME, APP_VERSION
from models import todo_table  # noqa: F401  (imported so Base knows about the todos table)
from routes.todo_routes import router as todo_router

# Create any missing tables in MySQL (existing tables and their data are left alone)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME, version=APP_VERSION, description=APP_DESCRIPTION)

# Register the todo routes with the app
app.include_router(todo_router)


@app.get("/")
def home():
    return {"message": f"Welcome to the {APP_NAME}! Visit /docs to try the API."}
```

- `Base.metadata.create_all(...)` looks at every class that inherits from `Base` and creates its table **if it doesn't exist yet**.
- `from models import todo_table` makes sure Python loads the `TodoTable` class before `create_all` runs. Without it, `Base` wouldn't know the table exists. (`# noqa: F401` just tells code checkers the import is intentional.)

### Step 11: Run it and check MySQL 🚀

1. Make sure MySQL is running in Laragon, XAMPP, WAMP or Herd.
2. Start the API:
   ```bash
   uvicorn main:app --reload
   ```
3. Open **http://127.0.0.1:8000/docs** and create a few todos with **POST `/todos/`**.
4. **Look at the data in MySQL.** In HeidiSQL or phpMyAdmin, open `todo_db` → `todos` → **Data** (or **Browse**). Your todos are there as rows! Or run:
   ```sql
   SELECT * FROM todos;
   ```
5. **The real test:** stop the server (`Ctrl + C`), start it again, and call **GET `/todos/`**. Your todos are still there. 🎉

The table MySQL created looks like this (`DESCRIBE todos;`):

| Field | Type | Null | Key | Extra |
|---|---|---|---|---|
| `id` | int | NO | PRI | auto_increment |
| `title` | varchar(255) | NO | | |
| `description` | text | YES | | |
| `completed` | tinyint(1) | NO | | |

> MySQL has no real boolean type, so `completed` is stored as `tinyint(1)`: `0` for false, `1` for true. SQLAlchemy converts it back to `True`/`False` for you.

---

## Testing Your API

### Option 1: Interactive docs (easiest)

Open **http://127.0.0.1:8000/docs** and try this sequence:

1. **POST `/todos/`** with this body:
   ```json
   { "title": "Learn FastAPI", "description": "Finish the tutorial" }
   ```
2. **GET `/todos/`**: you should see your new todo in the list.
3. **PUT `/todos/1`** with this body:
   ```json
   { "completed": true }
   ```
4. **GET `/todos/1`**: `completed` is now `true`.
5. **DELETE `/todos/1`**: you get `"Todo deleted successfully"`.
6. **GET `/todos/1`** again: you get a `404` with `"Todo not found"`.

There is also an alternative docs page at **http://127.0.0.1:8000/redoc**.

### Option 2: curl (from the terminal)

```bash
# Create
curl -X POST http://127.0.0.1:8000/todos/ -H "Content-Type: application/json" -d "{\"title\": \"Buy milk\"}"

# List all
curl http://127.0.0.1:8000/todos/

# Get one
curl http://127.0.0.1:8000/todos/1

# Update
curl -X PUT http://127.0.0.1:8000/todos/1 -H "Content-Type: application/json" -d "{\"completed\": true}"

# Delete
curl -X DELETE http://127.0.0.1:8000/todos/1
```

> On Windows PowerShell, use `curl.exe` instead of `curl`.

### Option 3: Postman or Thunder Client

[Postman](https://www.postman.com/) and the [Thunder Client](https://www.thunderclient.com/) VS Code extension let you send requests through a visual interface.

---

## Key Concepts Cheat Sheet

| Concept | Example | Explanation |
|---|---|---|
| **App** | `app = FastAPI()` | The main application object |
| **Route / Endpoint** | `@app.get("/")` | A URL + method the API responds to |
| **Router** | `APIRouter(prefix="/todos")` | Groups related routes; added to the app with `include_router` |
| **Path parameter** | `/todos/{todo_id}` | A value taken from the URL itself |
| **Query parameter** | `def list_todos(completed: bool = None)` | A function argument that is not in the path, e.g. `/todos/?completed=true` |
| **Request body** | `data: TodoCreate` | JSON sent by the client, validated by a Pydantic model |
| **Response model** | `response_model=Todo` | The shape of the data you send back |
| **Status code** | `status_code=201` | Tells the client what happened |
| **HTTPException** | `raise HTTPException(404, "...")` | Returns an error response |
| **Engine** | `create_engine(DATABASE_URL)` | The connection to the database |
| **Session** | `db: Session` | One "conversation" with the database; changes are saved on `db.commit()` |
| **Table model** | `class TodoTable(Base)` | A Python class that maps to a database table |
| **Dependency** | `db: Session = Depends(get_db)` | FastAPI runs `get_db()` and passes the result into the route |

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `uvicorn: command not found` / `'uvicorn' is not recognized` | Virtual environment not active, or uvicorn not installed | Activate `venv`, then `pip install "uvicorn[standard]"` |
| `ModuleNotFoundError: No module named 'fastapi'` | Packages installed outside the venv | Activate `venv` and run `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'models'` | Server started from the wrong folder | `cd` into the project folder (where `main.py` is) before running `uvicorn` |
| `Error loading ASGI app. Attribute "app" not found` | Wrong name in the command | Make sure `main.py` contains `app = FastAPI()` and you run `uvicorn main:app` |
| `[Errno 10048] address already in use` | Another server is using port 8000 | Stop the other server, or run `uvicorn main:app --reload --port 8001` |
| `422 Unprocessable Entity` | The request body doesn't match the model | Check the field names and types (e.g. `title` must be a string) |
| Changed `.env` but nothing changed | The server only reads `.env` at startup | Stop the server (`Ctrl + C`) and start it again |
| `ModuleNotFoundError: No module named 'dotenv'` | `python-dotenv` not installed | `pip install python-dotenv` (the import is `dotenv`, but the package is `python-dotenv`) |
| PowerShell: "running scripts is disabled" when activating venv | Windows script policy | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again |

### Database errors (Part 2)

| Error | Cause | Fix |
|---|---|---|
| `(2003, "Can't connect to MySQL server on '127.0.0.1' ...")` | MySQL isn't running, or is on a different port | Start MySQL in Laragon / XAMPP / WAMP / Herd. Check `DB_PORT` in `.env` (WAMP's MySQL is often `3308`) |
| `(1049, "Unknown database 'todo_db'")` | The database hasn't been created | Run `CREATE DATABASE todo_db;` ([Part 2, Step 2](#step-2-create-the-database)) |
| `(1045, "Access denied for user 'root'@'localhost'")` | Wrong user or password | Check `DB_USER` and `DB_PASSWORD` in `.env`, then restart the server |
| `'cryptography' package is required for sha256_password or caching_sha2_password auth methods` | MySQL 8 uses a secure login method | `pip install cryptography` |
| `ModuleNotFoundError: No module named 'pymysql'` | Driver not installed | `pip install pymysql` |
| MySQL won't start: "port 3306 in use" | Another MySQL (e.g. XAMPP *and* Laragon) is already running | Stop MySQL in the other tool first |
| Added a new column to `TodoTable` but MySQL doesn't have it (`Unknown column ...`) | `create_all` only creates **missing tables**; it never changes existing ones | While learning: drop the table (`DROP TABLE todos;`) and restart the server to recreate it. **This deletes its data.** Later, use Alembic (see [Next Steps](#next-steps)) |
| `ResponseValidationError` when returning a todo | `Todo` model can't read the database object | Make sure `model_config = ConfigDict(from_attributes=True)` is in the `Todo` class |

---

## Exercises: Build Something Similar

The best way to learn is to build. Try these, in order of difficulty.

### 🟢 Easy: extend the Todo API

1. Add a `priority` field (`"low"`, `"medium"`, `"high"`) to the todo models. Remember to add it to **both** `models/todo.py` and `models/todo_table.py`, then drop and recreate the table (see [Database errors](#database-errors-part-2)).
2. Add a query parameter so `GET /todos/?completed=true` returns only completed todos.
   *Hint: add `completed: Optional[bool] = None` as a function argument in the route, and use `.filter(TodoTable.completed == completed)` in the handler.*
3. Add a `DELETE /todos/` endpoint that clears all todos. *Hint: `db.query(TodoTable).delete()` then `db.commit()`.*

### 🟡 Medium: build a new API with the same structure

Use this project as a template and build a **Book Library API**:

| Folder | What to create |
|---|---|
| `models/book.py` | `BookCreate` (title, author, year), `BookUpdate`, `Book` (with `from_attributes=True`) |
| `models/book_table.py` | `BookTable` with `__tablename__ = "books"` |
| `handlers/book_handler.py` | CRUD functions using `db: Session` |
| `routes/book_routes.py` | A router with `prefix="/books"` |
| `constant/messages.py` | `BOOK_NOT_FOUND`, `BOOK_DELETED` |
| `main.py` | `from models import book_table` and `app.include_router(book_router)` |

**The recipe for any new resource** (books, notes, contacts, products and so on):

1. **API model** (Pydantic): what does one item look like? What do you need to create it? To update it?
2. **Table model** (SQLAlchemy): which columns does the table need?
3. **Handler**: write `get_all`, `get_by_id`, `create`, `update` and `delete` functions using `db`.
4. **Routes**: connect each handler function to a URL and HTTP method, with `db: Session = Depends(get_db)`.
5. **Register**: import the table model and add `app.include_router(...)` in `main.py`.

### 🔴 Harder

- Put **both** Todos and Books in the same app (two routers).
- Add validation, e.g. `title` must be at least 3 characters (look up Pydantic's `Field(min_length=3)`).
- Add a `created_at` timestamp to each todo. *Hint: `Column(DateTime, server_default=func.now())` lets MySQL fill it in.*
- Add an `author_id` to books and an `authors` table, then link them with a `ForeignKey`.

---

## Next Steps

When you are comfortable with this project, here is what to learn next:

1. **Database migrations.** Use [Alembic](https://alembic.sqlalchemy.org/) to change tables (add columns, etc.) without deleting your data.
2. **Automated tests.** Use `pytest` with FastAPI's `TestClient`.
3. **Typed settings.** Swap `python-dotenv` for `pydantic-settings`, which validates and converts `.env` values (e.g. strings to `int`/`bool`) for you.
4. **Authentication.** Protect endpoints with login and tokens (see the FastAPI security tutorial).
5. **Deployment.** Put your API online with Render, Railway or Docker.

### Useful Resources

- [Official FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), which is excellent and beginner friendly
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [FastAPI: SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [HTTP Status Codes Explained (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

Happy coding! 🚀
