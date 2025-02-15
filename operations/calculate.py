import asyncio

from database.db import get_exchange, update_formulas, get_formulas


def calculate_price(country_code, original_price, discounted_price):
    formula = get_formulas().get(country_code)
    exchange_rate = get_exchange()

    if "IN" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "NG" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "US" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)
        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "AR" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "TR" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    elif "UA" == country_code:
        original_price = original_price * exchange_rate.get(country_code)
        discounted_price = discounted_price * exchange_rate.get(country_code)

        if discounted_price > 2999:
            original_price += 200
            discounted_price += 200

        original_price = round(eval(str(original_price) + formula), -1)
        discounted_price = round(eval(str(discounted_price) + formula), -1)
        return original_price, discounted_price

    else:
        return f"error: Нет такой страны - {country_code}"

