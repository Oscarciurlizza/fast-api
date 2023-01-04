from fastapi import APIRouter
from fastapi import HTTPException

from ..database import Movie

from ..schemas import MovieResponseModel
from ..schemas import MovieRequestModel

router = APIRouter(prefix="/movies")


@router.post("", response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):

    if Movie.select().where(Movie.title == movie.title).exists():
        raise HTTPException(status_code=404, detail="Movie already exists")

    movie = Movie.create(
        title=movie.title
    )

    return movie
