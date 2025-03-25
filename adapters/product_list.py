from typing import TypeVar, List, Generic, Optional
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


class ProductListResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]


class DataAdapter:
    async def enrich_response(
        self,
        response: List[T],
        count: int,
        limit: int,
        offset: int,
        base_url: str = "/games/",
    ) -> ProductListResponse[T]:
        next_offset = offset + limit if offset + limit < count else None
        prev_offset = offset - limit if offset > 0 else None

        return ProductListResponse[T](
            count=count,
            next=f"{base_url}?limit={limit}&offset={next_offset}"
            if next_offset is not None
            else None,
            previous=f"{base_url}?limit={limit}&offset={prev_offset}"
            if prev_offset is not None
            else None,
            results=response,
        )
