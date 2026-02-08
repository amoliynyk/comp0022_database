from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/genres", tags=["genres"])


# --- Response Models ---

class GenreCount(BaseModel):
    genre: str
    movie_count: int
    avg_rating: Optional[float] = None


class GenrePopularity(BaseModel):
    genre: str
    total_ratings: int
    avg_rating: float
    unique_users: int


class GenrePolarisation(BaseModel):
    genre: str
    avg_rating: float
    std_dev: float
    polarisation_score: float


# --- Endpoints ---

@router.get("", response_model=list[GenreCount])
def list_genres():
    """List all genres with movie counts and average ratings."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/popularity", response_model=list[GenrePopularity])
def genre_popularity():
    """Genre popularity statistics (total ratings, unique users)."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/polarisation", response_model=list[GenrePolarisation])
def genre_polarisation():
    """Genre polarisation scores (high std-dev = polarising)."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")
