from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api_v1.routers.sales import router as sales_router
from api_v1.routers.all_games import router as all_games_router



app = FastAPI(root_path="/api-sale")

app.include_router(all_games_router)
app.include_router(sales_router)


def is_allowed_origin(origin: str) -> bool:
    allowed_origins = [
        "http://localhost:5173",
        "https://xbox-products.vercel.app",
    ]
    return origin in allowed_origins


app.add_middleware(
    CORSMiddleware,
    # allow_origin_func=is_allowed_origin,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
