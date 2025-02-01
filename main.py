from fastapi import FastAPI

from db import get_game_by_id, get_all_sale_product

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
