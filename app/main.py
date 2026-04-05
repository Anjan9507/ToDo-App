from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import task_route, auth_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "ToDo API is running!"}


app.include_router(task_route.router)
app.include_router(auth_route.router)

