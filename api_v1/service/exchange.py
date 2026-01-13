from datetime import date

import requests

from database.db import update_exchange


def get_new_exchange() -> None:
    rates_cb = get_ru_centr_bank()
    date_exchange = date.today().strftime("%d-%m-%Y")
    usd_to_rub = get_rate_cb(rates=rates_cb, code='USD')
    try_to_rub = get_rate_cb(rates=rates_cb, code='TRY')  # Турция
    ngn_to_rub = get_rate_cb(rates=rates_cb, code='NGN')  # Наира Нигерия
    ars_to_rub = get_ars()  # Песо Аргентины
    uah_to_rub = get_rate_cb(rates=rates_cb, code='UAH')  # Гривна Укр
    egp_to_rub = get_rate_cb(rates=rates_cb, code='EGP')  # Фунт Египет

    update_exchange(
        date_exchange=date_exchange,
        usd_to_rub=usd_to_rub,
        try_to_rub=try_to_rub,
        ngn_to_rub=ngn_to_rub,
        ars_to_rub=ars_to_rub,
        uah_to_rub=uah_to_rub,
        egp_to_rub=egp_to_rub,
    )


def get_rate_cb(rates: dict, code: str) -> float:
    val = rates.get(code)
    if not val:
        return -1
    return val["Value"] / val["Nominal"]


def get_ru_centr_bank():
    url = "https://www.cbr-xml-daily.ru/daily_json.js"

    response = requests.get(url=url)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        return data["Valute"]


def get_ars():
    url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/ars.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["ars"]["rub"]



if __name__ == "__main__":
    get_new_exchange()
