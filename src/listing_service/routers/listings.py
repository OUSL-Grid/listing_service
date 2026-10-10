from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from listing_service.schemas.listing import (
    ListingCreate,
    ListingResponse,
    ListingUpdate,
)
from listing_service.services.listing_service import ListingService

router = APIRouter()


@router.post(
    "/listings",
    response_model=ListingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new listing",
    description="Creates a new item listing. Requires verified student JWT.",
    responses={
        201: {"description": "Listing created successfully"},
        401: {"description": "Unauthorized — invalid or missing JWT"},
        422: {"description": "Validation error"},
    },
)
async def create_listing(
    payload: ListingCreate,
    service: ListingService = Depends(),
):
    """
    Create a new listing:
    
    - **title**: Item title (3-120 chars)
    - **description**: Detailed description (10-2000 chars)
    - **price_cents**: Price in cents (integer, >= 0)
    - **category**: textbook | lab-gear | dorm | other
    - **condition**: new | like-new | good | fair | poor
    """
    return await service.create(payload)


@router.get(
    "/listings",
    response_model=List[ListingResponse],
    summary="Search and filter listings",
)
async def search_listings(
    category: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    keyword: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    service: ListingService = Depends(),
):
    """Search listings with optional filters."""
    return await service.search(
        category=category,
        min_price=min_price,
        max_price=max_price,
        keyword=keyword,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/listings/{listing_id}",
    response_model=ListingResponse,
    summary="Get a single listing",
)
async def get_listing(
    listing_id: int,
    service: ListingService = Depends(),
):
    listing = await service.get(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.patch(
    "/listings/{listing_id}",
    response_model=ListingResponse,
    summary="Update a listing",
)
async def update_listing(
    listing_id: int,
    payload: ListingUpdate,
    service: ListingService = Depends(),
):
    return await service.update(listing_id, payload)