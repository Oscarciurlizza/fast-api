from fastapi import FastAPI

from fastapi import APIRouter
from fastapi import Depends

from fastapi import HTTPException
from fastapi import status


from fastapi.security import OAuth2PasswordRequestForm

from fastapi.middleware.cors import CORSMiddleware

from project.database import UserReview
from project.database import Movie

from project.database import User

from .routers import review_router
from .routers import movie_router
from .routers import user_router

from .common import create_access_token

from project.database import database as connection

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(title="Reviews Gio",
              description="Api that comment your opinion for any movie", version="1")

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)
api_v1.include_router(review_router)
api_v1.include_router(movie_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api_v1.post("/auth")
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)

    if user:
        return {
            "user": data.username,
            "access_token": create_access_token(user),
            "token_type": "Bearer",
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password incorrect",
            headers={"WWW-Authenticate": "Beraer"}
        )

app.include_router(api_v1)


@app.on_event("startup")
def startup():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User, Movie, UserReview])


@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()
