import os
import random
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from config import price_tables, price_groups
from operations.calculate import calculate_price
from schemas.product import ProductResponse

base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, "../db.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()


def get_random_products(product_ids, limit):
    count = len(product_ids)
    # Перемешиваем список случайным образом
    random.shuffle(product_ids)
    games = []
    for product_id in product_ids[:limit]:  # Ограничиваем по limit
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["prices"] = get_game_price(product_id)
            games.append(ProductResponse.from_db(game_data))

    return count, games


def update_exchange(
    date_exchange: str,
    usd_to_rub: float,
    try_to_rub: float,
    ngn_to_rub: float,
    ars_to_rub: float,
    uah_to_rub: float,
    egp_to_rub: float,
) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exchange (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_exchange TEXT,
            "IN" REAL,
            "NG" REAL,
            "US" REAL,
            "AR" REAL,
            "TR" REAL,
            "UA" REAL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM exchange")
    exists = cur.fetchone()[0] > 0
    if not exists:
        cur.execute(
            """INSERT INTO exchange (date_exchange, "IN", "NG", "US", "AR", "TR", "UA") VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                date_exchange,
                egp_to_rub,
                ngn_to_rub,
                usd_to_rub,
                ars_to_rub,
                try_to_rub,
                uah_to_rub,
            ),
        )
    else:
        cur.execute(
            """UPDATE exchange SET date_exchange = ?, "IN" = ?, "NG" = ?, "US" = ?, "AR" = ?, "TR" = ?, "UA" = ?""",
            (
                date_exchange,
                egp_to_rub,
                ngn_to_rub,
                usd_to_rub,
                ars_to_rub,
                try_to_rub,
                uah_to_rub,
            ),
        )

    conn.commit()


def get_exchange() -> dict[str, float]:
    cur.execute("SELECT * FROM exchange")
    result = cur.fetchone()
    if result is None:
        return {}

    columns = [desc[0] for desc in cur.description]

    exchange_rate = dict(zip(columns, result))

    return exchange_rate


def get_game_by_id(product_id: str) -> dict[str, Any]:
    cur.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    result = cur.fetchone()

    if result is None:
        return {}

    columns = [desc[0] for desc in cur.description]

    game_data = dict(zip(columns, result))

    return game_data


def get_game_with_prices_by_id(product_id: str) -> ProductResponse:
    game = get_game_by_id(product_id=product_id)
    prices = get_game_price(product_id=product_id)
    game["prices"] = prices
    return ProductResponse.from_db(game=game)


def get_games_with_limit(offset: int, limit: int) -> tuple[int, list[ProductResponse]]:
    cur.execute("SELECT product_id FROM products LIMIT ? OFFSET ?", (limit, offset))
    product_ids = [row[0] for row in cur.fetchall()]

    games = []
    for product_id in product_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["prices"] = get_game_price(product_id)
            games.append(ProductResponse.from_db(game_data))

    count = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]

    return count, games


def get_sale_games_with_limit(offset: int, limit: int) -> tuple[int, list[ProductResponse]]:
    cur.execute("SELECT product_id FROM products WHERE sale_product == 1 LIMIT ? OFFSET ?;", (limit, offset))
    product_ids = [row[0] for row in cur.fetchall()]

    games = []
    for product_id in product_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["prices"] = get_game_price(product_id)
            games.append(ProductResponse.from_db(game_data))

    count = cur.execute("SELECT COUNT(*) FROM products WHERE sale_product == 1").fetchone()[0]

    return count, games


def get_all_game_by_price(price: float = 1500) -> list:
    query = "SELECT product_id FROM products WHERE end_date_sale BETWEEN ? AND ?;"
    cur.execute(query, (0, price))

    result = []
    for product_id in cur.fetchall():
        result.append(product_id[0])

    return result


def get_price_by_product(product_id: str) -> dict[str, Any]:
    prices = {}

    for table in price_tables:
        cur.execute(f"SELECT * FROM '{table}' WHERE product_id = ?", (product_id,))
        result = cur.fetchall()

        if result:
            columns = [desc[0] for desc in cur.description]
            prices[table] = [dict(zip(columns, row)) for row in result]

    return prices


def get_prices_by_product(product_id) -> dict[str, Any]:
    prices = {}
    for table in price_tables:
        cur.execute(f"SELECT * FROM '{table}' WHERE product_id = ?", (product_id,))
        result = cur.fetchall()

        if result:
            columns = [desc[0] for desc in cur.description]
            country_prices = [dict(zip(columns, row)) for row in result]
            prices[table] = country_prices

        else:
            prices[table] = []

    new_price = {}

    for country_code, price_data_list in prices.items():
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

def update_formulas(country_name: str, formula: str) -> None:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS formulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "IN" TEXT,
            "NG" TEXT,
            "US" TEXT,
            "AR" TEXT,
            "TR" TEXT,
            "UA" TEXT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM formulas")
    exists = cur.fetchone()[0] > 0
    if not exists:
        cur.execute(
            f'''INSERT INTO formulas ("{country_name}") VALUES (?)''', (formula,)
        )
    else:
        cur.execute(f'''UPDATE formulas SET "{country_name}" = ?''', (formula,))

    conn.commit()


def get_formulas() -> dict[str, Any]:
    cur.execute("SELECT * FROM formulas")
    result = cur.fetchone()
    if result is None:
        return {}

    columns = [desc[0] for desc in cur.description]

    all_formulas = dict(zip(columns, result))

    return all_formulas


def get_minimal_price_by_product(product_id: str) -> dict[str, Any]:
    prices = {}

    cur.execute("SELECT * FROM minimal_price_game WHERE product_id = ?", (product_id,))
    result = cur.fetchall()

    if result:
        columns = [desc[0] for desc in cur.description]
        prices = [dict(zip(columns, row)) for row in result]

    return prices


def get_game_up_to_with_limit(limit: int, price: float = 1500) -> tuple[int, list[ProductResponse]]:
    result = []
    for region in price_tables:
        query = f'SELECT product_id, ru_price FROM "{region}" WHERE ru_price <= ?'
        cur.execute(query, (price,))

        for product_id, ru_price in cur.fetchall():
            if ru_price == 0:
                continue

            if product_id not in result:
                result.append(product_id)

    return get_random_products(product_ids=result,
                               limit=limit)


def get_game_price(product_id: str) -> dict[str, Any]:
    result = {}

    for group, regions in price_groups.items():
        min_price = float("inf")
        min_country = None
        discounted_percentage = None

        for region in regions:
            query = f'SELECT ru_price, discounted_percentage FROM "{region}" WHERE product_id = ?'
            cur.execute(query, (product_id,))

            rows = cur.fetchall()
            valid_rows = [(row[0], row[1]) for row in rows if row[0] > 0]

            if valid_rows:
                local_min, local_discounted_percentage = min(
                    valid_rows, key=lambda x: x[0]
                )

                if local_min < min_price:
                    min_price = local_min
                    min_country = region
                    discounted_percentage = local_discounted_percentage

        result[group] = {
            "country": min_country if min_country else None,
            "price": min_price if min_price != float("inf") and min_price > 0 else -1,
            "discounted_percentage": round(discounted_percentage, 0)
            if discounted_percentage is not None
            else None,
        }

    return result


def get_product_ids_with_dlc(limit: int) -> tuple[int, list[ProductResponse]]:
    query = """SELECT product_id FROM products WHERE dlc IS NOT NULL AND dlc <> '';"""
    cur.execute(query)
    product_ids = [row[0] for row in cur.fetchall()]

    return get_random_products(product_ids=product_ids,
                               limit=limit)


def get_product_ids_with_audio_ru(limit: int) -> tuple[int, list[ProductResponse]]:
    query = """SELECT product_id FROM products WHERE audio_ru == 1 ;"""
    cur.execute(query)
    product_ids = [row[0] for row in cur.fetchall()]

    return get_random_products(product_ids=product_ids,
                               limit=limit)


def get_product_ids_with_pc(limit: int) -> tuple[int, list[ProductResponse]]:
    query = """SELECT product_id FROM products WHERE device LIKE '%PC%';"""
    cur.execute(query)
    product_ids = [row[0] for row in cur.fetchall()]
    return get_random_products(product_ids=product_ids,
                               limit=limit)


def get_games_by_recent_releases(days: int, offset: int, limit: int) -> tuple[int, list[ProductResponse]]:
    date_limit = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # => SQL-запрос для поиска игр, чья дата релиза позже или равна рассчитанному лимиту, но не позже завтрашнего дня
    # => и сортировка по дате релиза в порядке убывания
    query = """SELECT product_id
               FROM products 
               WHERE release_date >= ? AND release_date < ?
               ORDER BY release_date DESC
               LIMIT ? OFFSET ?;"""
    cur.execute(query, (date_limit, tomorrow, limit, offset))

    product_ids = [row[0] for row in cur.fetchall()]
    games = []
    for product_id in product_ids:
        game_data = get_game_by_id(product_id)
        if game_data:
            game_data["prices"] = get_game_price(product_id)
            games.append(ProductResponse.from_db(game_data))

    count = cur.execute("SELECT COUNT(*) FROM products WHERE release_date >= ? AND release_date < ?", (date_limit, tomorrow,)).fetchone()[0]

    return count, games


def get_products_by_discount(min_percentage: float,
                             max_percentage: float,
                             limit: int,
                             ) -> tuple[int, list[ProductResponse]]:

    products_with_discount = []
    for group, regions in price_groups.items():
        for region in regions:
            query = f'SELECT product_id, discounted_percentage FROM "{region}"'
            cur.execute(query)

            rows = cur.fetchall()

            for product_id, discounted_percentage in rows:
                if (
                    discounted_percentage is not None
                    and min_percentage <= discounted_percentage <= max_percentage
                ):
                    products_with_discount.append(product_id)

    return get_random_products(limit=limit, product_ids=products_with_discount)

