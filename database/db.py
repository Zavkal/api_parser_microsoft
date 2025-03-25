import os
import sqlite3
from datetime import datetime, timezone, timedelta

from config import regions_id, price_tables, price_groups

base_dir = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(base_dir, '../db.db')

conn = sqlite3.connect(db_path)
cur = conn.cursor()


def update_exchange(date_exchange: str,
                    usd_to_rub: float,
                    try_to_rub: float,
                    ngn_to_rub: float,
                    ars_to_rub: float,
                    uah_to_rub: float,
                    egp_to_rub: float):
    cur.execute('''
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
    ''')

    cur.execute("SELECT COUNT(*) FROM exchange")
    exists = cur.fetchone()[0] > 0
    if not exists:
        cur.execute(
            '''INSERT INTO exchange (date_exchange, "IN", "NG", "US", "AR", "TR", "UA") VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (date_exchange, egp_to_rub, ngn_to_rub, usd_to_rub, ars_to_rub, try_to_rub, uah_to_rub))
    else:
        cur.execute(
            '''UPDATE exchange SET date_exchange = ?, "IN" = ?, "NG" = ?, "US" = ?, "AR" = ?, "TR" = ?, "UA" = ?''',
            (date_exchange, egp_to_rub, ngn_to_rub, usd_to_rub, ars_to_rub, try_to_rub, uah_to_rub))

    conn.commit()


def get_exchange():
    cur.execute('SELECT * FROM exchange')
    result = cur.fetchone()
    if result is None:
        return 0

    # Получение имен колонок
    columns = [desc[0] for desc in cur.description]

    # Создание словаря с данными
    exchange_rate = dict(zip(columns, result))

    return exchange_rate


def get_game_by_id(product_id: str):
    cur.execute('SELECT * FROM products WHERE product_id = ?', (product_id,))
    result = cur.fetchone()

    if result is None:
        return {"error": "Game not found"}

    # Получение имен колонок
    columns = [desc[0] for desc in cur.description]

    # Создание словаря с данными
    game_data = dict(zip(columns, result))

    return game_data


def get_all_sale_product():
    # Запрос для выборки данных
    cur.execute('SELECT product_id FROM products WHERE sale_product == 1;')

    result = []
    for url in cur.fetchall():
        result.append(url[0])

    return result


def get_all_game_by_price(price: float = 1500):
    # Запрос для выборки данных
    query = 'SELECT product_id FROM products WHERE end_date_sale BETWEEN ? AND ?;'
    # Выполняем запрос с подстановкой дат
    cur.execute(query, (0, price))

    result = []
    for product_id in cur.fetchall():
        result.append(product_id[0])

    return result


def get_price_by_product(product_id):
    prices = {}

    for table in price_tables:
        cur.execute(f"SELECT * FROM '{table}' WHERE product_id = ?", (product_id,))
        result = cur.fetchall()

        if result:
            columns = [desc[0] for desc in cur.description]
            prices[table] = [dict(zip(columns, row)) for row in result]

    return prices


def get_prices_by_product(product_id):
    prices = {}
    for table in price_tables:
        cur.execute(f"SELECT * FROM '{table}' WHERE product_id = ?", (product_id,))
        result = cur.fetchall()

        if result:
            columns = [desc[0] for desc in cur.description]
            country_prices = [dict(zip(columns, row)) for row in result]
            prices[table] = country_prices

        else:
            prices[table] = []  # Если нет данных, возвращаем пустой список

    return prices


def update_formulas(country_name: str, formula: str):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS formulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            "IN" TEXT,
            "NG" TEXT,
            "US" TEXT,
            "AR" TEXT,
            "TR" TEXT,
            "UA" TEXT
        )
    ''')

    cur.execute("SELECT COUNT(*) FROM formulas")
    exists = cur.fetchone()[0] > 0
    if not exists:
        cur.execute(f'''INSERT INTO formulas ("{country_name}") VALUES (?)''',
                    (formula,))
    else:
        cur.execute(
            f'''UPDATE formulas SET "{country_name}" = ?''',
            (formula,))

    conn.commit()


def get_formulas():
    cur.execute('SELECT * FROM formulas')
    result = cur.fetchone()
    if result is None:
        return 0

    # Получение имен колонок
    columns = [desc[0] for desc in cur.description]

    # Создание словаря с данными
    all_formulas = dict(zip(columns, result))

    return all_formulas


def get_minimal_price_by_product(product_id):
    prices = {}

    cur.execute(f"SELECT * FROM minimal_price_game WHERE product_id = ?", (product_id,))
    result = cur.fetchall()

    if result:
        columns = [desc[0] for desc in cur.description]
        prices = [dict(zip(columns, row)) for row in result]

    return prices


def get_game_up_to(price: int):
    result = []
    for region in price_tables:
        query = f'SELECT product_id, ru_price FROM "{region}" WHERE ru_price <= ?'
        cur.execute(query, (price,))

        for product_id, ru_price in cur.fetchall():
            # Игнорируем продукт, если его цена равна нулю
            if ru_price == 0:
                continue

            # Добавляем product_id в список, если цена подходит
            if product_id not in result:
                result.append(product_id)

    return result


def get_game_price(product_id: str):
    result = {}

    for group, regions in price_groups.items():
        min_price = float("inf")
        min_country = None
        discounted_percentage = None  # Инициализация

        for region in regions:
            query = f'SELECT ru_price, discounted_percentage FROM "{region}" WHERE product_id = ?'
            cur.execute(query, (product_id,))

            # Извлекаем все строки и фильтруем только те, где цена больше нуля
            rows = cur.fetchall()
            valid_rows = [(row[0], row[1]) for row in rows if row[0] > 0]

            if valid_rows:
                # Находим минимальную цену и соответствующий процент скидки
                local_min, local_discounted_percentage = min(valid_rows, key=lambda x: x[0])

                if local_min < min_price:
                    min_price = local_min
                    min_country = region
                    discounted_percentage = local_discounted_percentage

        # Если так и не нашли цену, или нашли < 0, ставим -1
        result[group] = {
            "country": min_country if min_country else None,
            "price": min_price if min_price != float("inf") and min_price > 0 else -1,
            "discounted_percentage": round(discounted_percentage, 0) if discounted_percentage is not None else None
        }

    return result


def get_product_ids_with_dlc():
    query = '''SELECT product_id FROM products WHERE dlc IS NOT NULL AND dlc <> '';'''
    cur.execute(query)
    return [row[0] for row in cur.fetchall()]


def get_product_ids_with_audio_ru():
    query = '''SELECT product_id FROM products WHERE audio_ru == 1 ;'''
    cur.execute(query)
    return [row[0] for row in cur.fetchall()]


def get_product_ids_with_pc():
    query = '''SELECT product_id FROM products WHERE device LIKE '%PC%';'''
    cur.execute(query)
    return [row[0] for row in cur.fetchall()]


def get_games_by_recent_releases(days: int):
    # Рассчитываем дату, которая будет являться ограничением для поиска
    date_limit = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    # Рассчитываем дату завтрашнего дня для ограничения
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # SQL-запрос для поиска игр, чья дата релиза позже или равна рассчитанному лимиту, но не позже завтрашнего дня
    # и сортировка по дате релиза в порядке убывания
    query = '''SELECT product_id
               FROM products 
               WHERE release_date >= ? AND release_date < ?
               ORDER BY release_date DESC;'''
    cur.execute(query, (date_limit, tomorrow))

    # Возвращаем результаты в виде списка игр
    return [row[0] for row in cur.fetchall()]


def get_products_by_discount(min_percentage: float, max_percentage: float):
    products_with_discount = []

    # Проходим по всем группам и регионам
    for group, regions in price_groups.items():
        for region in regions:
            query = f'SELECT product_id, discounted_percentage FROM "{region}"'
            cur.execute(query)

            # Извлекаем все строки
            rows = cur.fetchall()

            for product_id, discounted_percentage in rows:
                if discounted_percentage is not None and min_percentage <= discounted_percentage <= max_percentage:
                    products_with_discount.append(product_id)

    return products_with_discount





