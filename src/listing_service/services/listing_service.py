from typing import List, Optional
from listing_service.schemas.listing import (
    ListingCreate, ListingUpdate, ListingResponse,
)


class ListingService:
    async def create(self, payload: ListingCreate) -> ListingResponse:
        # TODO: implement in another issue
        raise NotImplementedError

    async def search(
        self,
        category: Optional[str] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        keyword: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> List[ListingResponse]:
        # TODO: implement in another issue
        raise NotImplementedError

    async def get(self, listing_id: int):
        # TODO: implement in another issue
        raise NotImplementedError

    async def update(self, listing_id: int, payload: ListingUpdate):
        # TODO: implement in another issue
        raise NotImplementedError