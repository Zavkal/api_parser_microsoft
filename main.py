import random

from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware

from adapters.product_list import DataAdapter, ProductListResponse
from database.db import get_game_with_prices_by_id, get_games_with_limit
from database.db import (
    get_game_by_id,
    get_all_sale_product,
    get_prices_by_product,
    get_game_up_to,
    get_game_price,
    get_product_ids_with_dlc,
    get_product_ids_with_audio_ru,
    get_product_ids_with_pc,
    get_games_by_recent_releases,
    get_products_by_discount,
)
from operations.calculate import calculate_price
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


@app.get("/game_price/{product_id}")
async def game_price(product_id: str):
    all_price = get_prices_by_product(product_id)
    new_price = {}

    for country_code, price_data_list in all_price.items():
        if not price_data_list:
            new_price[country_code] = {}
            continue

        for price_data in price_data_list:
            orig_price, disc_price = calculate_price(
                original_price=price_data.get("original_price"),
                discounted_price=price_data.get("discounted_price"),
                country_code=country_code,
            )

            new_price[country_code] = {
                "original_price": orig_price,
                "discounted_price": disc_price,
                "discounted_percentage": round(
                    price_data.get("discounted_percentage"), 1
                ),
            }

    return new_price


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


@app.get("/games/sales/")
async def get_sale_games(offset: int = 0, limit: int = 10):
    product_ids = get_all_sale_product()
    count = len(product_ids)
    paginated_ids = product_ids[offset : offset + limit]

    games = []
    for product_id in paginated_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/sales/?limit={limit}&offset={next_offset}"
        if next_offset is not None
        else None,
        "previous": f"/games/sales/?limit={limit}&offset={prev_offset}"
        if prev_offset is not None
        else None,
        "results": games,
    }


@app.get("/games/up_to")
async def games_up_to(price: int = 500, limit: int = 10):
    all_game_up_to = get_game_up_to(price)
    count = len(all_game_up_to)

    # Перемешиваем список случайным образом
    random.shuffle(all_game_up_to)

    # Ограничиваем список количеством товаров, которое указано в limit
    games = []
    for product_id in all_game_up_to[:limit]:  # Ограничиваем по limit
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    return {"count": count, "results": games}


@app.get("/games/dlc")
async def games_dlc(limit: int = 10):
    all_game = get_product_ids_with_dlc()
    count = len(all_game)

    # Перемешиваем список случайным образом
    random.shuffle(all_game)

    # Ограничиваем список количеством товаров, которое указано в limit
    games = []
    for product_id in all_game[:limit]:  # Ограничиваем по limit
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    return {"count": count, "results": games}


@app.get("/games/audio_ru")
async def games_audio_ru(limit: int = 10):
    all_game = get_product_ids_with_audio_ru()
    count = len(all_game)

    # Перемешиваем список случайным образом
    random.shuffle(all_game)

    # Ограничиваем список количеством товаров, которое указано в limit
    games = []
    for product_id in all_game[:limit]:  # Ограничиваем по limit
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    return {"count": count, "results": games}


@app.get("/games/device_pc")
async def games_device_pc(limit: int = 10):
    all_game = get_product_ids_with_pc()
    count = len(all_game)

    # Перемешиваем список случайным образом
    random.shuffle(all_game)

    # Ограничиваем список количеством товаров, которое указано в limit
    games = []
    for product_id in all_game[:limit]:  # Ограничиваем по limit
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    return {"count": count, "results": games}


@app.get("/games/recent_releases")
async def games_recent_releases(days: int = 15, offset: int = 0, limit: int = 10):
    product_ids = get_games_by_recent_releases(days)
    count = len(product_ids)
    paginated_ids = product_ids[offset : offset + limit]

    games = []
    for product_id in paginated_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/recent_releases/?limit={limit}&offset={next_offset}"
        if next_offset is not None
        else None,
        "previous": f"/games/recent_releases/?limit={limit}&offset={prev_offset}"
        if prev_offset is not None
        else None,
        "results": games,
    }


@app.get("/games/by_discount")
async def games_by_discount(
    min_percentage: float = 75,
    max_percentage: float = 100,
    offset: int = 0,
    limit: int = 10,
):
    product_ids = get_products_by_discount(min_percentage, max_percentage)
    count = len(product_ids)
    random.shuffle(product_ids)
    paginated_ids = product_ids[offset : offset + limit]

    games = []
    for product_id in paginated_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["price"] = get_game_price(product_id)
            games.append(game_data)

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/by_discount/?limit={limit}&offset={next_offset}"
        if next_offset is not None
        else None,
        "previous": f"/games/by_discount/?limit={limit}&offset={prev_offset}"
        if prev_offset is not None
        else None,
        "results": games,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
