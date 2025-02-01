import sqlite3
from datetime import datetime, timezone, timedelta

db_path = "db.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()


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





























