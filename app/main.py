from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import task_route, auth_route

from slowapi.middleware import SlowAPIMiddleware
from app.core.rate_limiter import limiter, rate_limit_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

@app.get("/")
def root():
    return {"message": "ToDo API is running!"}


app.include_router(task_route.router)
app.include_router(auth_route.router)

