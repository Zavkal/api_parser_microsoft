import asyncio

import requests

from database.db import update_exchange


def get_new_exchange():
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD,TRY,NGN,ARS,UAH,EGP&base=RUB"

    payload = {}
    headers = {
        "apikey": "JY1QPAEUMi6k65jnMJt902P3FheHW11A"
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        date_exchange = data["date"]
        usd_to_rub = 1 / data['rates'].get('USD', 'Нет данных')  # Доллар
        try_to_rub = 1 / data['rates'].get('TRY', 'Нет данных')  # Турция
        ngn_to_rub = 1 / data['rates'].get('NGN', 'Нет данных')  # Наира Нигерия
        ars_to_rub = 1 / data['rates'].get('ARS', 'Нет данных')  # Песо Аргентины
        uah_to_rub = 1 / data['rates'].get('UAH', 'Нет данных')  # Гривна Укр
        egp_to_rub = 1 / data['rates'].get('EGP', 'Нет данных')  # Фунт Египет

        update_exchange(date_exchange=date_exchange,
                        usd_to_rub=usd_to_rub,
                        try_to_rub=try_to_rub,
                        ngn_to_rub=ngn_to_rub,
                        ars_to_rub=ars_to_rub,
                        uah_to_rub=uah_to_rub,
                        egp_to_rub=egp_to_rub,
                        )
    else:
        print(response.text)


if __name__ == '__main__':
    get_new_exchange()
