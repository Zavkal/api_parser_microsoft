import random

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.db import get_game_by_id, get_all_sale_product, get_prices_by_product, get_exchange, get_game_up_to, \
    get_game_price, get_product_ids_with_dlc, get_product_ids_with_audio_ru, get_product_ids_with_pc, \
    get_games_by_recent_releases, get_products_by_discount
from operations.calculate import calculate_price
from database.db import cur, conn


app = FastAPI(root_path="/api-sale")


def is_allowed_origin(origin: str) -> bool:
    allowed_origins = [
        "http://localhost:5173",
        "https://xbox-products.vercel.app",
    ]
    return origin in allowed_origins


app.add_middleware(
    CORSMiddleware,
    # allow_origin_func=is_allowed_origin,  # Динамическая проверка
    allow_origins=['*'],  # Динамическая проверка
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/game_id/{product_id}")
async def one_game_for_game_id(product_id: str):
    result = get_game_by_id(product_id)
    price = get_game_price(product_id)
    result['price'] = price
    return result

# @app.get("/game_sale/")
# async def all_sale_game():
#     return get_all_sale_product()


@app.get("/game_price/{product_id}")
async def game_price(product_id: str):
    all_price = get_prices_by_product(product_id)
    new_price = {}

    # Проходим по всем странам и данным
    for country_code, price_data_list in all_price.items():
        # Проверяем, есть ли данные для этой страны
        if not price_data_list:
            new_price[country_code] = {}  # Если данных нет, добавляем пустой список
            continue

        # Для каждой страны может быть несколько записей, обрабатываем их
        for price_data in price_data_list:
            orig_price, disc_price = calculate_price(
                original_price=price_data.get("original_price"),
                discounted_price=price_data.get('discounted_price'),
                country_code=country_code,
            )

            # Обновляем данные с новыми ценами и скидками
            new_price[country_code] = {
                'original_price': orig_price,
                'discounted_price': disc_price,
                'discounted_percentage': round(price_data.get('discounted_percentage'), 1),
            }

    return new_price


@app.get("/games/")
async def get_games(offset: int = 0, limit: int = 10):
    cur.execute("SELECT product_id FROM products LIMIT ? OFFSET ?", (limit, offset))
    product_ids = [row[0] for row in cur.fetchall()]

    games = []
    for product_id in product_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["prices"] = get_game_price(product_id)
            games.append(game_data)

    count = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/?limit={limit}&offset={next_offset}" if next_offset is not None else None,
        "previous": f"/games/?limit={limit}&offset={prev_offset}" if prev_offset is not None else None,
        "results": games
    }


@app.get("/games/sales/")
async def get_sale_games(offset: int = 0, limit: int = 10):
    product_ids = get_all_sale_product()
    count = len(product_ids)
    paginated_ids = product_ids[offset:offset + limit]

    games = []
    for product_id in paginated_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/sales/?limit={limit}&offset={next_offset}" if next_offset is not None else None,
        "previous": f"/games/sales/?limit={limit}&offset={prev_offset}" if prev_offset is not None else None,
        "results": games
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
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    return {
        "count": count,
        "results": games
    }


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
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    return {
        "count": count,
        "results": games
    }


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
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    return {
        "count": count,
        "results": games
    }


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
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    return {
        "count": count,
        "results": games
    }


@app.get("/games/recent_releases")
async def games_recent_releases(days: int = 15, offset: int = 0, limit: int = 10):
    product_ids = get_games_by_recent_releases(days)
    count = len(product_ids)
    paginated_ids = product_ids[offset:offset + limit]

    games = []
    for product_id in paginated_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/recent_releases/?limit={limit}&offset={next_offset}" if next_offset is not None else None,
        "previous": f"/games/recent_releases/?limit={limit}&offset={prev_offset}" if prev_offset is not None else None,
        "results": games
    }


@app.get("/games/by_discount")
async def games_by_discount(min_percentage: float = 75,
                                max_percentage: float = 100,
                                offset: int = 0, limit: int = 10):
    product_ids = get_products_by_discount(min_percentage, max_percentage)
    count = len(product_ids)
    random.shuffle(product_ids)
    paginated_ids = product_ids[offset:offset + limit]

    games = []
    for product_id in paginated_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data['price'] = get_game_price(product_id)
            games.append(game_data)

    next_offset = offset + limit if offset + limit < count else None
    prev_offset = offset - limit if offset > 0 else None

    return {
        "count": count,
        "next": f"/games/by_discount/?limit={limit}&offset={next_offset}" if next_offset is not None else None,
        "previous": f"/games/by_discount/?limit={limit}&offset={prev_offset}" if prev_offset is not None else None,
        "results": games
    }




















