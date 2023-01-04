from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from typing import List

from ..database import User
from ..database import Movie
from ..database import UserReview

from ..schemas import ReviewResponseModel
from ..schemas import ReviewsRequestModel
from ..schemas import ReviewRequestPutModel

from ..common import get_current_user

router = APIRouter(prefix="/reviews")


@router.post("", response_model=ReviewResponseModel)
async def create_reviews(user_review: ReviewsRequestModel, user: User = Depends(get_current_user)):

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    user_review = UserReview.create(
        user_id=user.id,  # owner
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )

    return user_review


@router.get("", response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(
        page, limit)  # SELECT * FROM user_reviews

    return [user_review for user_review in reviews]


@router.get("/{review_id}", response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return user_review


@router.put("/{review_id}", response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel, user: User = Depends(get_current_user)):

    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not the owner")

    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()

    return user_review


@router.delete("/{review_id}", response_model=ReviewResponseModel)
async def delete_review(review_id: int, user: User = Depends(get_current_user)):
    user_review = UserReview.select().where(UserReview.id == review_id).first()

    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    if user_review.user_id != user.id:
        raise HTTPException(status_code=401, detail="You are not the owner")

    user_review.delete_instance()

    return user_review
