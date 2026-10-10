from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from listing_service.db import Base
from listing_service.schemas.listing import (
    ListingCategory,
    ListingCondition,
    ListingStatus,
)


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seller_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[str] = mapped_column(
        Enum(ListingCategory, name="listing_category"), nullable=False
    )
    condition: Mapped[str] = mapped_column(
        Enum(ListingCondition, name="listing_condition"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        Enum(ListingStatus, name="listing_status"),
        default=ListingStatus.active,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )