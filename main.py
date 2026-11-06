# main.py
# The entry point of the app. It creates the FastAPI app and plugs in the routes.
# Run it with:  uvicorn main:app --reload

from fastapi import FastAPI

from configs.settings import APP_DESCRIPTION, APP_NAME, APP_VERSION
from routes.todo_routes import router as todo_router

app = FastAPI(title=APP_NAME, version=APP_VERSION, description=APP_DESCRIPTION)

# Register the todo routes with the app
app.include_router(todo_router)


@app.get("/")
def home():
    return {"message": f"Welcome to the {APP_NAME}! Visit /docs to try the API."}
