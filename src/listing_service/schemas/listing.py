from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ListingCategory(str, Enum):
    textbook = "textbook"
    lab_gear = "lab-gear"
    dorm = "dorm"
    other = "other"


class ListingCondition(str, Enum):
    new = "new"
    like_new = "like-new"
    good = "good"
    fair = "fair"
    poor = "poor"


class ListingStatus(str, Enum):
    active = "active"
    pending = "pending"
    sold = "sold"
    flagged = "flagged"
    removed = "removed"


class ListingCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=10, max_length=2000)
    price_cents: int = Field(..., ge=0)
    category: ListingCategory
    condition: ListingCondition

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Calculus Textbook 8th Ed",
                    "description": "Barely used, no highlights. Stewart edition.",
                    "price_cents": 2500,
                    "category": "textbook",
                    "condition": "like-new",
                }
            ]
        }
    }


class ListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=120)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    price_cents: Optional[int] = Field(None, ge=0)
    category: Optional[ListingCategory] = None
    condition: Optional[ListingCondition] = None


class ListingResponse(BaseModel):
    id: int
    seller_id: int
    title: str
    description: str
    price_cents: int
    category: ListingCategory
    condition: ListingCondition
    status: ListingStatus
    created_at: datetime

    model_config = {"from_attributes": True}