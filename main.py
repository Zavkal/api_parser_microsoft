from fastapi import FastAPI

from database.db import get_game_by_id, get_all_sale_product, get_prices_by_product, start_api_db

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/game_id/{game_id}")
async def one_game_for_game_id(game_id: str):

    return get_game_by_id(game_id)


@app.get("/game_sale/")
async def all_sale_game():

    return get_all_sale_product()


@app.get("/game_price/{product_id}")
async def game_price(product_id: str):

    return get_prices_by_product(product_id)


if __name__ == '__main__':
    start_api_db()
