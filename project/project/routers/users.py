from fastapi import APIRouter

from fastapi import Cookie
from fastapi import Response
from fastapi import Depends


from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from typing import List

from ..database import User

from ..schemas import UserResponseModel
from ..schemas import UserRequestModel

from ..schemas import ReviewResponseModel

from ..common import oauth2_schema
from ..common import get_current_user

router = APIRouter(prefix="/users")


@router.post("", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, "The username is already in use.")

    hash_password = User.hash_password(user.password)

    user = User.create(
        username=user.username,
        password=hash_password
    )

    return user


@router.post("/login", response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.password != User.hash_password(credentials.password):
        raise HTTPException(status_code=404, detail="User not found.")

    response.set_cookie(key="user_id", value=user.id)
    return user

""" @router.get("/reviews", response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return [user_review for user_review in user.reviews]
 """


@router.get("/reviews", response_model=List[ReviewResponseModel])
async def get_reviews(user: User = Depends(get_current_user)):

    return [user_review for user_review in user.reviews]
