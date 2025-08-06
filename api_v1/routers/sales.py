from fastapi import APIRouter, Depends

from api_v1.adapters.product_list import DataAdapter, ProductListResponse, ProductRandomListResponse
from database.db import get_sale_games_with_limit, get_sale_dlc_with_limit, get_products_by_discount
from api_v1.schemas.product import ProductResponse

router = APIRouter(prefix="/sales", tags=["Распродажи"])

@router.get(
    path="/",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Игры распродажи с пагинацией",
)
async def get_sale_games(offset: int = 0,
                         limit: int = 10,
                         data_adapter: DataAdapter = Depends()
                         ) -> ProductListResponse[ProductResponse]:
    count, games = get_sale_games_with_limit(limit=limit, offset=offset)

    return await data_adapter.enrich_response(
        response=games,
        count=count,
        limit=limit,
        offset=offset,
        base_url="/games/sales/",
    )


@router.get(
    path="/dlc",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="DLC игр и доп услуги с пагинацией")
async def games_dlc(offset: int = 0,
                    limit: int = 10,
                    data_adapter: DataAdapter = Depends()
                    ) -> ProductListResponse[ProductResponse]:
    count, games = get_sale_dlc_with_limit(
        offset=offset,
        limit=limit,
    )

    return await data_adapter.enrich_response(
        response=games,
        count=count,
        limit=limit,
        offset=offset,
        base_url="/games/sales/"
    )


@router.get("/games/by_discount",
         response_model_exclude_none=False,
         response_model_exclude_unset=False,
         summary="Товары по размеру скидки (РАНДОМ)")
async def games_by_discount(
        min_percentage: float = 75,
        max_percentage: float = 100,
        limit: int = 10,
        data_adapter: DataAdapter = Depends()
) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_products_by_discount(min_percentage, max_percentage, limit)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games
    )