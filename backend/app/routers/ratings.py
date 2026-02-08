from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/ratings", tags=["ratings"])


# --- Response Models ---

class RatingPattern(BaseModel):
    user_id: int
    total_ratings: int
    avg_rating: float
    std_dev: float
    genres_rated: int


class CrossGenrePreference(BaseModel):
    genre_a: str
    genre_b: str
    correlation: float
    shared_users: int


class LowRater(BaseModel):
    user_id: int
    avg_rating: float
    total_ratings: int
    pct_below_avg: float


class RatingConsistency(BaseModel):
    genre: str
    avg_std_dev: float
    most_consistent_pct: float
    least_consistent_pct: float


# --- Endpoints ---

@router.get("/patterns", response_model=list[RatingPattern])
def rating_patterns(
    limit: int = Query(50, ge=1, le=500),
    min_ratings: int = Query(10, ge=1),
):
    """Rating behaviour patterns across users."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/cross-genre", response_model=list[CrossGenrePreference])
def cross_genre_preferences(
    min_shared_users: int = Query(10, ge=1),
):
    """Cross-genre preference correlations."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/low-raters", response_model=list[LowRater])
def low_raters(
    threshold: float = Query(2.5, ge=0, le=5),
    limit: int = Query(50, ge=1, le=500),
):
    """Identify users who consistently rate below average."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/consistency", response_model=list[RatingConsistency])
def rating_consistency():
    """Rating consistency analysis per genre."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")
