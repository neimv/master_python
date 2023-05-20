
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from config.database import engine, Base
from jwt_manager import create_token
from middleware.error_handler import ErrorHandler
from routers.movie import movie_router


app = FastAPI()
app.title = 'My API'
app.version = '0.0.1'
app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    username: str
    password: str


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Welcome to my API</h1>')


@app.post("/login", tags=['auth'])
def login(user: User):
    if user.username == "user" and user.password == "password":
        token = create_token(user.dict())

        return JSONResponse(content=token, status_code=200)
