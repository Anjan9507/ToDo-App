from fastapi import FastAPI
from app.routes import task_route, auth_route

app = FastAPI()

@app.get("/")
def root():
    return {"message": "ToDo API is running!"}


app.include_router(task_route.router)
app.include_router(auth_route.router)

