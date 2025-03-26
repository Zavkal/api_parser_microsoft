import requests

from database.db import update_exchange
from dotenv import load_dotenv
import os


load_dotenv()
API_EXCHANGE = os.getenv('API_EXCHANGE')


def get_new_exchange() -> None:
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=USD,TRY,NGN,ARS,UAH,EGP&base=RUB"

    payload = {}
    headers = {"apikey": API_EXCHANGE}
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        date_exchange = data["date"]
        usd_to_rub = 1 / data["rates"].get("USD", -1)  # Доллар
        try_to_rub = 1 / data["rates"].get("TRY", -1)  # Турция
        ngn_to_rub = 1 / data["rates"].get("NGN", -1)  # Наира Нигерия
        ars_to_rub = 1 / data["rates"].get("ARS", -1)  # Песо Аргентины
        uah_to_rub = 1 / data["rates"].get("UAH", -1)  # Гривна Укр
        egp_to_rub = 1 / data["rates"].get("EGP", -1)  # Фунт Египет

        update_exchange(
            date_exchange=date_exchange,
            usd_to_rub=usd_to_rub,
            try_to_rub=try_to_rub,
            ngn_to_rub=ngn_to_rub,
            ars_to_rub=ars_to_rub,
            uah_to_rub=uah_to_rub,
            egp_to_rub=egp_to_rub,
        )


if __name__ == "__main__":
    get_new_exchange()
