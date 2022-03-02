
from typing import Optional
from enum import Enum

from pydantic import BaseModel
from pydantic import Field
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()


# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blond = "blond"
    red = "red"


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    # Para llenar datos de pruebas
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Neimv",
                "last_name": "Zatara",
                "age": 21,
                "hair_color": "black",
                "is_married": True
            }
        }


class Location(BaseModel):
    city: str
    state: str
    country: str


@app.get('/')
def home():
    return {"hello": "World"}


# Request and response body
@app.post('/person/new')
def create_person(person: Person = Body(...)):

    return person


# Validation query
@app.get('/person/detail')
def show_person(
            name: Optional[str] = Query(
                default=None,
                min_length=1,
                max_length=50,
                title="Person Name",
                description="This is the persona name."
            ),
            age: str = Query(
                ...,
                title="Person age",
                description="This is the person age"
            )  # Estos siempre deben ser opt (query para)
        ):
    return {name: age}


# Validations path parameters
@app.get("/person/detail/{person_id}")
def show_person_detail(
            person_id: int = Path(..., gt=0)
        ):
    return {person_id: "It exist"}


# Valitacion, request body
@app.put("/person/{person_id}")
def update_person(
            person_id: int = Path(
                ...,
                title="Person ID",
                description="this is the person ID",
                gt=0
            ),
            person: Person = Body(...),
            location: Location = Body(...)
        ):
    result = person.dict()
    result.update(location.dict())

    return result


# 
