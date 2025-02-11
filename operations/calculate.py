import asyncio

async def calculate_price(country_code, original_price, discounted_price):
    amount_usd = 20
    amount_try = 20

    usd_in_rub = amount_usd * usd_to_rub
    try_in_rub = amount_try * try_to_rub
    ngn_in_rub = ngn_to_rub * amount_usd
    ars_in_rub = ars_to_rub * amount_usd
    uah_in_rub = uah_to_rub * amount_usd
    egp_in_rub = egp_to_rub * amount_usd

    print(f"{amount_usd} USD = {usd_in_rub:.2f} RUB")
    print(f"{amount_try} TRY = {try_in_rub:.2f} RUB")
    print(f"{amount_try} ngn = {ngn_in_rub:.2f} RUB")
    print(f"{amount_try} ars = {ars_in_rub:.2f} RUB")
    print(f"{amount_try} uah = {uah_in_rub:.2f} RUB")
    print(f"{amount_try} egp = {egp_in_rub:.2f} RUB")
    if "IN" == country_code:
        return (original_price + discounted_price) / 2

    elif "NG" == country_code:
        return (original_price + discounted_price) / 2

    elif "US" == country_code:
        return (original_price + discounted_price) / 2

    elif "AR" == country_code:
        return (original_price + discounted_price) / 2

    elif "TR" == country_code:
        return (original_price + discounted_price) / 2

    elif "UA" == country_code:
        return (original_price + discounted_price) / 2

    else:
        return f"error: Нет такой страны - {country_code}"

