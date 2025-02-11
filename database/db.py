import sqlite3
from datetime import datetime, timezone, timedelta

from config import regions_id, price_tables
from operations.calculate import calculate_price

db_path = "../db.db"

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
            USD TEXT,
            TRY REAL,
            NGN REAL,
            ARS REAL,
            UAH REAL,
            EGP REAL
        )
    ''')

    cur.execute("SELECT COUNT(*) FROM exchange")
    exists = cur.fetchone()[0] > 0
    if not exists:
        cur.execute('''INSERT INTO exchange (date_exchange, USD, TRY, NGN, ARS, UAH, EGP) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    (date_exchange, usd_to_rub, try_to_rub, ngn_to_rub, ars_to_rub, uah_to_rub, egp_to_rub))
    else:
        cur.execute(
            '''UPDATE exchange SET date_exchange = ?, USD = ?, TRY = ?, NGN = ?, ARS = ?, UAH = ?, EGP = ?''',
            (date_exchange, usd_to_rub, try_to_rub, ngn_to_rub, ars_to_rub, uah_to_rub, egp_to_rub))


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

            for price_data in country_prices:
                price_data['calculated_price'] = calculate_price(country, price_data['original_price'],
                                                                 price_data['discounted_price'])

            prices[country] = country_prices
        else:
            prices[country] = []  # Если нет данных, возвращаем пустой список

    return prices
