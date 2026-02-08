from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/movies", tags=["movies"])


# --- Response Models ---

class MovieSummary(BaseModel):
    movie_id: int
    title: str
    genres: list[str]
    avg_rating: Optional[float] = None
    num_ratings: int = 0


class MovieList(BaseModel):
    movies: list[MovieSummary]
    total: int
    page: int
    page_size: int


class MovieDetail(BaseModel):
    movie_id: int
    title: str
    genres: list[str]
    avg_rating: Optional[float] = None
    num_ratings: int = 0
    year: Optional[int] = None
    tags: list[str] = []


class RatingDistribution(BaseModel):
    movie_id: int
    title: str
    distribution: dict[str, int]
    avg_rating: float
    num_ratings: int


# --- Endpoints ---

@router.get("", response_model=MovieList)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    title: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    sort: str = Query("title", pattern="^(title|rating|year|num_ratings)$"),
):
    """Paginated movie list with optional filters."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{movie_id}", response_model=MovieDetail)
def get_movie(movie_id: int):
    """Single movie detail including tags."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{movie_id}/ratings", response_model=RatingDistribution)
def get_movie_ratings(movie_id: int):
    """Rating distribution for a movie (e.g. count per star bucket)."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")
