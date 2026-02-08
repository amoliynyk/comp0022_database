from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/personality", tags=["personality"])


# --- Response Models ---

class TraitStats(BaseModel):
    trait: str
    mean: float
    std_dev: float
    min: float
    max: float
    count: int


class TraitGenreCorrelation(BaseModel):
    trait: str
    genre: str
    correlation: float
    p_value: float
    sample_size: int


class UserSegment(BaseModel):
    segment_id: int
    label: str
    size: int
    dominant_traits: dict[str, float]
    preferred_genres: list[str]


# --- Endpoints ---

@router.get("/traits", response_model=list[TraitStats])
def personality_traits():
    """Big Five personality trait statistics across users."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/genre-correlation", response_model=list[TraitGenreCorrelation])
def trait_genre_correlation(
    trait: Optional[str] = None,
    genre: Optional[str] = None,
):
    """Correlation between personality traits and genre preferences."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/segments", response_model=list[UserSegment])
def user_segments(
    n_segments: int = Query(5, ge=2, le=20),
):
    """Cluster users into segments based on personality and rating behaviour."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")
