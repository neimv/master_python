
from fastapi import FastAPI, Body, Path, Query, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request

from jwt_manager import create_token, validate_token


app = FastAPI()
app.title = 'My API'
app.version = '0.0.1'


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        
        if data["username"] != "user":
            raise HTTPException(status_code=403, detail="credenciales invalidas")


class User(BaseModel):
    username: str
    password: str


class Movie(BaseModel):
    id_movie: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id_movie": 1,
                "title": "mi peli",
                "overview": "description de la peli",
                "year": 2020,
                "rating": 9.0,
                "category": "Drama",
            }
        }


movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }
]


@app.get('/', tags=['Home'])
def message():
    return HTMLResponse('<h1>Welcome to my API</h1>')


@app.post("/login", tags=['auth'])
def login(user: User):
    if user.username == "user" and user.password == "password":
        token = create_token(user.dict())

        return JSONResponse(content=token, status_code=200)


@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get('/movies/{movie_id}', tags=['movies'], status_code=200)
def get_movie(movie_id: int = Path(ge=1, le=2000)):
    clean_movies = [movie for movie in movies if movie['id'] == movie_id]

    if clean_movies:
        return JSONResponse(content=clean_movies[0], status_code=200)

    return JSONResponse(status_code=404, content=[])


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [movie for movie in movies if movie['category'] == category]


@app.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)

    return movies


@app.put('/movies/{movie_id}', tags=['movies'])
def update_movie(
    movie_id: int,
    movie: Movie):
    clean_movies = [movie for movie in movies if movie['id'] == movie_id]

    if clean_movies:
        index = movies.index(clean_movies[0])
        movies[index] = {
            'id': movie_id,
            'title': movie.title,
            'overview': movie.overview,
            'year': movie.year,
            'rating': movie.rating,
            'category': movie.category,
        }
        return movies[index]

    return {}


@app.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(movie_id: int):
    clean_movies = [movie for movie in movies if movie['id'] == movie_id]

    if clean_movies:
        movies.remove(clean_movies[0])
        return clean_movies[0]

    return {}
