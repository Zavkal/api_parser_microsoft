import os
import sqlite3
from datetime import datetime, timezone, timedelta

from config import regions_id, price_tables

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


def get_all_sale_product(days=7):
    current_date = datetime.now(timezone.utc)
    future_date = current_date + timedelta(days=days)

    # Запрос для выборки данных
    query = 'SELECT product_id FROM products WHERE end_date_sale BETWEEN ? AND ?;'
    # Выполняем запрос с подстановкой дат
    cur.execute(query, (current_date.strftime("%Y-%m-%d"), future_date.strftime("%Y-%m-%d")))

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
    for country, table in regions_id.items():
        cur.execute(f"SELECT * FROM '{table}' WHERE product_id = ?", (product_id,))
        result = cur.fetchall()

        if result:
            columns = [desc[0] for desc in cur.description]
            country_prices = [dict(zip(columns, row)) for row in result]
            prices[country] = country_prices

        else:
            prices[country] = []  # Если нет данных, возвращаем пустой список

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
    pass