from fastapi import FastAPI
from app.api.routes import users_router, tasks_router, auth_router

app = FastAPI(title="Task Manager API")


app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"status": "ok"}
