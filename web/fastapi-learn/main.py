
from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


app = FastAPI()
app.title = 'My API'
app.version = '0.0.1'
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


@app.get('/movies', tags=['movies'])
def get_movies():
    return movies


@app.get('/movies/{movie_id}', tags=['movies'])
def get_movie(movie_id: int):
    clean_movies = [movie for movie in movies if movie['id'] == movie_id]

    if clean_movies:
        return clean_movies[0]

    return []


@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    return [movie for movie in movies if movie['category'] == category]


@app.post('/movies', tags=['movies'])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()):
    movies.append({
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    })

    return movies


@app.put('/movies/{movie_id}', tags=['movies'])
def update_movie(
    movie_id: int,
    title: str = Body(),
    overview: str = Body(),
    year: int = Body(),
    rating: float = Body(),
    category: str = Body()):
    clean_movies = [movie for movie in movies if movie['id'] == movie_id]

    if clean_movies:
        index = movies.index(clean_movies[0])
        movies[index] = {
            'id': movie_id,
            'title': title,
            'overview': overview,
            'year': year,
            'rating': rating,
            'category': category
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
