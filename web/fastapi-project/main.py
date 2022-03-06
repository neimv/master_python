
from typing import List

from fastapi import FastAPI, status

from models import UserBase, User, Tweet


app = FastAPI()


# Path operations
# Users
@app.post(
        '/sigup',
        response_model=User,
        response_model_exclude={"password"},
        status_code=status.HTTP_201_CREATED,
        summary="Register a User",
        tags=["Users"]
    )
def signup():
    pass


@app.post(
        '/login',
        response_model=User,
        response_model_exclude={"password"},
        status_code=status.HTTP_200_OK,
        summary="Login a User",
        tags=["Users"]
    )
def login():
    pass


@app.get(
        '/users',
        response_model=List[User],
        response_model_exclude={"password"},
        status_code=status.HTTP_200_OK,
        summary="Shw all User",
        tags=["Users"]
    )
def show_all_users():
    pass


@app.get(
        '/users/{user_id}',
        response_model=User,
        response_model_exclude={"password"},
        status_code=status.HTTP_200_OK,
        summary="Show a user",
        tags=["Users"]
    )
def show_a_user():
    pass


@app.delete(
        '/users/{user_id}/delete',
        response_model=User,
        response_model_exclude={"password"},
        status_code=status.HTTP_200_OK,
        summary="Delete a User",
        tags=["Users"]
    )
def delete_a_user():
    pass


@app.put(
        '/user/{user_id}/update',
        response_model=User,
        response_model_exclude={"password"},
        status_code=status.HTTP_200_OK,
        summary="Update a User",
        tags=["Users"]
    )
def update_a_user():
    pass


# Tweets
@app.get(
        path="/",
        response_model=List[Tweet],
        status_code=status.HTTP_200_OK,
        summary="Show all tweets",
        tags=["Tweets"]
    )
def home():
    return {"Twitter API": "V0.0.1"}


@app.post(
        '/post',
        response_model=Tweet,
        status_code=status.HTTP_201_CREATED,
        summary="Post a tweet",
        tags=["Tweets"]
    )
def post():
    pass


@app.get(
        path="/tweets/{tweet_id}",
        response_model=Tweet,
        status_code=status.HTTP_200_OK,
        summary="Show a tweet",
        tags=["Tweets"]
    )
def show_a_tweet():
    pass


@app.delete(
        path="/tweets/{tweet_id}/delete",
        response_model=Tweet,
        status_code=status.HTTP_200_OK,
        summary="Delete a tweet",
        tags=["Tweets"]
    )
def delete_a_tweet():
    pass


@app.put(
        path="/tweets/{tweet_id}/update",
        response_model=Tweet,
        status_code=status.HTTP_200_OK,
        summary="Update a tweet",
        tags=["Tweets"]
    )
def update_a_tweet():
    pass

