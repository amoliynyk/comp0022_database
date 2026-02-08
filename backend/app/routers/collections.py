from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.auth.schemas import UserInfo
from app.auth.users import get_current_user

router = APIRouter(prefix="/api/collections", tags=["collections"])


# --- Request / Response Models ---

class CollectionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None


class CollectionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None


class CollectionSummary(BaseModel):
    collection_id: int
    name: str
    description: Optional[str]
    movie_count: int
    created_at: datetime


class CollectionDetail(BaseModel):
    collection_id: int
    name: str
    description: Optional[str]
    movies: list[dict]
    created_at: datetime
    updated_at: Optional[datetime] = None


class AddMovie(BaseModel):
    movie_id: int


# --- Endpoints ---

@router.get("", response_model=list[CollectionSummary])
def list_collections(current_user: UserInfo = Depends(get_current_user)):
    """List all collections for the authenticated user."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("", response_model=CollectionSummary, status_code=status.HTTP_201_CREATED)
def create_collection(
    data: CollectionCreate,
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a new collection."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{collection_id}", response_model=CollectionDetail)
def get_collection(
    collection_id: int,
    current_user: UserInfo = Depends(get_current_user),
):
    """Get collection detail with its movies."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.put("/{collection_id}", response_model=CollectionSummary)
def update_collection(
    collection_id: int,
    data: CollectionUpdate,
    current_user: UserInfo = Depends(get_current_user),
):
    """Update collection name or description."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_id: int,
    current_user: UserInfo = Depends(get_current_user),
):
    """Delete a collection."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{collection_id}/movies", status_code=status.HTTP_201_CREATED)
def add_movie_to_collection(
    collection_id: int,
    data: AddMovie,
    current_user: UserInfo = Depends(get_current_user),
):
    """Add a movie to a collection."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")


@router.delete("/{collection_id}/movies/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_movie_from_collection(
    collection_id: int,
    movie_id: int,
    current_user: UserInfo = Depends(get_current_user),
):
    """Remove a movie from a collection."""
    # TODO: implement once DB schema is finalised
    raise HTTPException(status_code=501, detail="Not implemented")
