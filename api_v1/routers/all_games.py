from fastapi import APIRouter, HTTPException, Depends

from api_v1.adapters.product_list import DataAdapter, ProductRandomListResponse, ProductListResponse
from database.db import get_game_with_prices_by_id, search_games_by_title, get_prices_by_product, get_games_with_limit, \
    get_game_up_to_with_limit, get_product_ids_with_audio_ru, get_product_ids_with_pc, get_games_by_recent_releases
from api_v1.schemas.product import ProductResponse

router = APIRouter(prefix="/games", tags=["Все продукты"])


@router.get(
    path="/game_id/{product_id}",
    response_model=ProductResponse,
    summary="Товар по его product_id",
)
async def game_by_product_id(product_id: str) -> ProductResponse:
    game = get_game_with_prices_by_id(product_id=product_id)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    return game


@router.get(
    path="/search/{partial_title}",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Поиск по совпадению названия",
)
async def games_by_search_title(
        title: str,
        data_adapter: DataAdapter = Depends()
) -> ProductRandomListResponse[ProductResponse]:
    count, games = search_games_by_title(title)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games
    )


@router.get(
    path="/game_price/{product_id}",
    summary="Я вообще хз, надо оно нам или нет.",
)
async def game_price(product_id: str):
    return get_prices_by_product(product_id)


@router.get(
    path="/",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Список игр с пагинацией",
)
async def get_games(
        offset: int = 0,
        limit: int = 10,
        data_adapter: DataAdapter = Depends(),
) -> ProductListResponse[ProductResponse]:
    count, games = get_games_with_limit(limit=limit, offset=offset)

    return await data_adapter.enrich_response(
        response=games,
        count=count,
        limit=limit,
        offset=offset,
        base_url="/",
    )


@router.get(
    path="/up_to",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Игры до определенной цены (РАНДОМ)",
)
async def games_up_to(price: int = 500,
                      limit: int = 10,
                      data_adapter: DataAdapter = Depends()
                      ) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_game_up_to_with_limit(limit=limit, price=price)
    return await data_adapter.enrich_response_without_offset(
        response=games,
        count=count,
    )


@router.get(
    path="/audio_ru",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Игры с русской озвучкой (РАНДОМ)",
)
async def games_audio_ru(limit: int = 10,
                         data_adapter: DataAdapter = Depends()
                         ) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_product_ids_with_audio_ru(limit)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games
    )


@router.get(
    path="/device_pc",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Игры на компьютер (РАНДОМ)",
)
async def games_device_pc(limit: int = 10,
                          data_adapter: DataAdapter = Depends()
                          ) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_product_ids_with_pc(limit)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games
    )


@router.get(
    path="/recent_releases",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="Последние релизы (От свежих к старым)",
)
async def games_recent_releases(days: int = 15,
                                offset: int = 0,
                                limit: int = 10,
                                data_adapter: DataAdapter = Depends()
                                ) -> ProductListResponse[ProductResponse]:
    count, games = get_games_by_recent_releases(days=days,
                                                offset=offset,
                                                limit=limit)

    return await data_adapter.enrich_response(
        count=count,
        response=games,
        limit=limit,
        offset=offset,
        base_url="recent_releases"
    )
