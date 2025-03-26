from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware

from adapters.product_list import DataAdapter, ProductListResponse, ProductRandomListResponse
from database.db import (
    get_game_with_prices_by_id,
    get_games_with_limit,
    get_game_up_to_with_limit,
    get_sale_games_with_limit,
    get_prices_by_product,
    get_product_ids_with_dlc,
    get_product_ids_with_audio_ru,
    get_product_ids_with_pc,
    get_games_by_recent_releases,
    get_products_by_discount,
)
from schemas.product import ProductResponse

app = FastAPI(root_path="/api-sale")


def is_allowed_origin(origin: str) -> bool:
    allowed_origins = [
        "http://localhost:5173",
        "https://xbox-products.vercel.app",
    ]
    return origin in allowed_origins


app.add_middleware(
    CORSMiddleware,
    # allow_origin_func=is_allowed_origin,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/game_id/{product_id}",
    response_model=ProductResponse,
    summary="Отдает продукт в едином экземпляре",
)
async def game_by_product_id(product_id: str) -> ProductResponse:
    game = get_game_with_prices_by_id(product_id=product_id)
    if not game:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    return game


@app.get("/game_price/{product_id}",
         summary="Я вообще хз, надо оно нам или нет.")
async def game_price(product_id: str):
    return get_prices_by_product(product_id)


@app.get(
    "/games/",
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
        base_url="/games/",
    )


@app.get(
    "/games/sales/",
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


@app.get(
    "/games/up_to",
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


@app.get(
    "/games/dlc",
    response_model_exclude_none=False,
    response_model_exclude_unset=False,
    summary="DLC игр и доп услуги (РАНДОМ)")
async def games_dlc(limit: int = 10,
                    data_adapter: DataAdapter = Depends()
                    ) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_product_ids_with_dlc(limit)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games)


@app.get("/games/audio_ru",
         response_model_exclude_none=False,
         response_model_exclude_unset=False,
         summary="Игры с русской озвучкой (РАНДОМ)")
async def games_audio_ru(limit: int = 10,
                         data_adapter: DataAdapter = Depends()
                         ) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_product_ids_with_audio_ru(limit)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games
    )


@app.get("/games/device_pc",
         response_model_exclude_none=False,
         response_model_exclude_unset=False,
         summary="Игры на компьютер (РАНДОМ)")
async def games_device_pc(limit: int = 10,
                          data_adapter: DataAdapter = Depends()
                          ) -> ProductRandomListResponse[ProductResponse]:
    count, games = get_product_ids_with_pc(limit)

    return await data_adapter.enrich_response_without_offset(
        count=count,
        response=games
    )


@app.get("/games/recent_releases",
         response_model_exclude_none=False,
         response_model_exclude_unset=False,
         summary="Последние релизы (От свежих к старым)")
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
        base_url="/games/recent_releases"
    )


@app.get("/games/by_discount",
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
