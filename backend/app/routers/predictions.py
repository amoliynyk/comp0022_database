from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


# --- Request / Response Models ---

class PredictionRequest(BaseModel):
    title: str
    genres: list[str]
    year: Optional[int] = None


class PredictionResponse(BaseModel):
    predicted_rating: float
    confidence: float
    similar_titles: list[str] = []


class SimilarMovie(BaseModel):
    movie_id: int
    title: str
    similarity_score: float
    genres: list[str]
    avg_rating: Optional[float] = None


# --- Endpoints ---

@router.post("/predict", response_model=PredictionResponse)
def predict_rating(data: PredictionRequest):
    """Predict the rating for a hypothetical new title based on genre and metadata."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/similar/{movie_id}", response_model=list[SimilarMovie])
def similar_movies(movie_id: int, limit: int = Query(10, ge=1, le=100)):
    """Find movies similar to the given movie based on ratings and genre overlap."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")
