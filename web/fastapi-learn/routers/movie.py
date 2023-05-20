

from fastapi import Path, Query, Depends, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional, List

from config.database import Session
from models.movie import Movie as MovieModel
from middleware.jwt_bearer import JWTBearer


movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=15, min_length=5)
    overview: str = Field(max_length=50, min_length=15)
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
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


@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/{movie_id}', tags=['movies'], status_code=200)
def get_movie(movie_id: int = Path(ge=1, le=2000)):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not result:
        return JSONResponse(content={"message": "No se encontraron resultados"}, status_code=400)

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [movie for movie in movies if movie['category'] == category]


@movie_router.post('/movies', tags=['movies'])
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()

    return movies


@movie_router.put('/movies/{movie_id}', tags=['movies'])
def update_movie(
    movie_id: int,
    movie: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not result:
        return JSONResponse(content={"message": "No se encontraron resultados"}, status_code=400)

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    db.commit()

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.delete('/movies/{movie_id}', tags=['movies'])
def delete_movie(movie_id: int):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not result:
        return JSONResponse(content={"message": "No se encontraron resultados"}, status_code=400)

    db.delete(result)
    db.commit()

    return {}
