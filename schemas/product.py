from typing import Optional
from pydantic import BaseModel


class PriceInfo(BaseModel):
    country: Optional[str] = None
    price: Optional[float] = 0
    discounted_percentage: Optional[float] = 0


class PricesSchema(BaseModel):
    key: PriceInfo
    u_acc: PriceInfo
    new_acc: PriceInfo


class ProductResponse(BaseModel):
    id: int
    product_id: str
    game_name: Optional[str] = None
    url_product: Optional[str] = None
    end_date_sale: Optional[str] = None
    device: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    developer_name: Optional[str] = None
    publisher_name: Optional[str] = None
    image_url: Optional[str] = None
    pass_product_id: Optional[str] = None
    release_date: Optional[str] = None
    capabilities: Optional[str] = None
    category: Optional[str] = None
    link_video: Optional[str] = None
    link_screenshot: Optional[str] = None
    game_weight: Optional[int] = None
    audio_ru: Optional[int] = None
    interface_ru: Optional[int] = None
    subtitles_ru: Optional[int] = None
    sale_product: Optional[int] = None
    dlc: Optional[str] = None
    prices: Optional[PricesSchema] = None

    @classmethod
    def from_db(cls, game: dict) -> "ProductResponse":
        return cls(
            id=game["id"],
            product_id=game["product_id"],
            url_product=game.get("url_product", ""),
            game_name=game.get("game_name", ""),
            end_date_sale=game.get("end_date_sale", ""),
            device=game.get("device", ""),
            description=game.get("description", ""),
            short_description=game.get("short_description", ""),
            developer_name=game.get("developer_name", ""),
            publisher_name=game.get("publisher_name", ""),
            image_url=game.get("image_url", ""),
            pass_product_id=game.get("pass_product_id", ""),
            release_date=game.get("release_date", ""),
            capabilities=game.get("capabilities", ""),
            category=game.get("category", ""),
            link_video=game.get("link_video"),
            link_screenshot=game.get("link_screenshot", ""),
            game_weight=game.get("game_weight", 0),
            audio_ru=game.get("audio_ru", 0),
            interface_ru=game.get("interface_ru", 0),
            subtitles_ru=game.get("subtitles_ru", 0),
            sale_product=game.get("sale_product", 0),
            dlc=game.get("dlc", ""),
            prices=PricesSchema(
                key=PriceInfo(
                    country=game["prices"]["key"].get("country", ""),
                    price=game["prices"]["key"]["price"],
                    discounted_percentage=game["prices"]["key"].get(
                        "discounted_percentage", 0
                    ),
                ),
                u_acc=PriceInfo(
                    country=game["prices"]["u_acc"].get("country", ""),
                    price=game["prices"]["u_acc"]["price"],
                    discounted_percentage=game["prices"]["u_acc"].get(
                        "discounted_percentage", 0
                    ),
                ),
                new_acc=PriceInfo(
                    country=game["prices"]["new_acc"].get("country", ""),
                    price=game["prices"]["new_acc"]["price"],
                    discounted_percentage=game["prices"]["new_acc"].get(
                        "discounted_percentage", 0
                    ),
                ),
            ),
        )
