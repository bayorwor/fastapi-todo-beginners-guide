# Todo API with FastAPI: A Beginner's Tutorial

This project is a small **Todo API** built with [FastAPI](https://fastapi.tiangolo.com/), a Python framework for building backend APIs.

You can use it in two ways:

1. **Run it** and play with a working API in your browser.
2. **Rebuild it yourself**, step by step, by following the [tutorial](#build-it-yourself-step-by-step) below.

By the end you will know how to:

- Set up a Python project with a virtual environment
- Organise a FastAPI project into clear folders
- Describe your data with Pydantic models
- Build the 5 basic API operations: **Create, Read, Update, Delete** (CRUD)
- Return proper errors (like `404 Not Found`)
- Test your API with the interactive docs FastAPI builds for you

---

## Table of Contents

- [What is an API?](#what-is-an-api)
- [Prerequisites](#prerequisites)
- [Quick Start (run the finished project)](#quick-start-run-the-finished-project)
- [Project Structure](#project-structure)
- [How a Request Flows](#how-a-request-flows)
- [Environment Variables (.env)](#environment-variables-env)
- [The Endpoints](#the-endpoints)
- [Build It Yourself, Step by Step](#build-it-yourself-step-by-step)
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

**4. Create your `.env` file** by copying the template:

```bash
# Windows (PowerShell)
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

You can open `.env` and change `APP_NAME` to see the title on the `/docs` page change. See [Environment Variables](#environment-variables-env) for more.

**5. Start the server:**

```bash
uvicorn main:app --reload
```

- `main` is the file `main.py`
- `app` is the `FastAPI()` object inside that file
- `--reload` restarts the server every time you save a file

**6. Open the interactive docs** at **http://127.0.0.1:8000/docs**

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
│   └── settings.py          # Loads app settings from .env
├── constant/
│   ├── __init__.py
│   └── messages.py          # Reusable text, e.g. "Todo not found"
├── models/
│   ├── __init__.py
│   └── todo.py              # The SHAPE of our data (what a Todo looks like)
├── handlers/
│   ├── __init__.py
│   └── todo_handler.py      # The LOGIC: create, read, update, delete
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
| `configs/` | Loads app settings from `.env` | The restaurant's **name and opening hours** |

> **What is `__init__.py`?** It is an empty file that tells Python "this folder is a package", so you can import from it, e.g. `from models.todo import Todo`.

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
   │   handlers/   │  Creates the todo and saves it in the list
   └──────┬────────┘
          ▼
   Response: 201 Created
   {"id": 1, "title": "Buy milk", "description": null, "completed": false}
```

---

## Environment Variables (`.env`)

Settings like the app name, or later a database password, should **not** be written directly in your code. They go in a `.env` file instead:

```env
APP_NAME=Todo API
APP_VERSION=1.0.0
APP_DESCRIPTION=A simple Todo API built with FastAPI for learning.
```

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

## Build It Yourself, Step by Step

Follow these steps in a **new, empty folder** to recreate the project from scratch. Type the code yourself rather than copying it. You will learn much more that way.

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

> ⚠️ **The data disappears when the server restarts.** The list only lives in memory. That's fine for learning. Later you can replace this file with database code, and the routes won't need to change.

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

---

## Exercises: Build Something Similar

The best way to learn is to build. Try these, in order of difficulty.

### 🟢 Easy: extend the Todo API

1. Add a `priority` field (`"low"`, `"medium"`, `"high"`) to the todo models.
2. Add a query parameter so `GET /todos/?completed=true` returns only completed todos.
   *Hint: add `completed: Optional[bool] = None` as a function argument in the route.*
3. Add a `DELETE /todos/` endpoint that clears all todos.

### 🟡 Medium: build a new API with the same structure

Use this project as a template and build a **Book Library API**:

| Folder | What to create |
|---|---|
| `models/book.py` | `BookCreate` (title, author, year), `BookUpdate`, `Book` |
| `handlers/book_handler.py` | CRUD functions using a list |
| `routes/book_routes.py` | A router with `prefix="/books"` |
| `constant/messages.py` | `BOOK_NOT_FOUND`, `BOOK_DELETED` |
| `main.py` | `app.include_router(book_router)` |

**The recipe for any new resource** (books, notes, contacts, products and so on):

1. **Model**: what does one item look like? What do you need to create it? To update it?
2. **Handler**: write `get_all`, `get_by_id`, `create`, `update` and `delete` functions.
3. **Routes**: connect each handler function to a URL and HTTP method.
4. **Register**: add `app.include_router(...)` in `main.py`.

### 🔴 Harder

- Put **both** Todos and Books in the same app (two routers).
- Add validation, e.g. `title` must be at least 3 characters (look up Pydantic's `Field(min_length=3)`).
- Add a `created_at` timestamp to each todo.

---

## Next Steps

When you are comfortable with this project, here is what to learn next:

1. **A real database.** Replace the list with SQLite using [SQLModel](https://sqlmodel.tiangolo.com/) so data survives restarts.
2. **Automated tests.** Use `pytest` with FastAPI's `TestClient`.
3. **Typed settings.** Swap `python-dotenv` for `pydantic-settings`, which validates and converts `.env` values (e.g. strings to `int`/`bool`) for you.
4. **Authentication.** Protect endpoints with login and tokens (see the FastAPI security tutorial).
5. **Deployment.** Put your API online with Render, Railway or Docker.

### Useful Resources

- [Official FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/), which is excellent and beginner friendly
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [HTTP Status Codes Explained (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

---

Happy coding! 🚀
