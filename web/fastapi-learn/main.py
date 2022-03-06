
from typing import Optional
from enum import Enum

from pydantic import BaseModel
from pydantic import Field, EmailStr
from fastapi import FastAPI, Body, Query, Path, status, Form, Header, Cookie, UploadFile, File, HTTPException

app = FastAPI()


# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blond = "blond"
    red = "red"


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)


class Person(PersonBase):
    password: str = Field(..., min_length=8)

    # Para llenar datos de pruebas
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Neimv",
    #             "last_name": "Zatara",
    #             "age": 21,
    #             "hair_color": "black",
    #             "is_married": True
    #         }
    #     }


class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city: str
    state: str
    country: str


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="holi")
    message: str = Field(default="Login successfully")


@app.get('/', status_code=status.HTTP_200_OK)
def home():
    return {"hello": "World"}


# Request and response body
@app.post(
        '/person/new',
        response_model=PersonOut,
        status_code=status.HTTP_201_CREATED,
        tags=["Persons"],
        summary="Create person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    - Title: Create Person

    - Description: This path operation creates a person in the app
      and save the information in the database

    - Parameters:
        - Request body parameter:
            - **person: Person** -> A person model with first name
              last name, hair color, age and is_married
    - Result: Return a person model with first name, last name, age
      hair color and marital status
    """

    return person


# Validation query
@app.get(
        '/person/detail',
        status_code=status.HTTP_200_OK,
        tags=["Persons"],
        deprecated=True
    )
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
@app.get("/person/detail/{person_id}", tags=["Persons"])
def show_person_detail(
            person_id: int = Path(..., gt=0)
        ):
    tmp_register = [1, 2, 3, 4, 5]

    if person_id not in tmp_register:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )

    return {person_id: "It exist"}


# Valitacion, request body
@app.put("/person/{person_id}", tags=["Persons"])
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


# Forms
@app.post(path="/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


# Cookies and headers
@app.post(path="/contact", status_code=status.HTTP_200_OK)
def contact(
            first_name: str = Form(..., max_length=20, min_length=1),
            last_name: str = Form(..., max_length=20, min_length=1),
            email: EmailStr = Form(...),
            message: str = Form(..., min_length=20),
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None)
        ):
    return user_agent


# Upload files
@app.post("/post-image")
def post_image(image: UploadFile = File(...)):
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kb)': round(len(image.file.read()) / 1024, ndigits=2)
    }
