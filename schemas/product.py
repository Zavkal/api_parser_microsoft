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
    title: Optional[str] = None
    url_product: Optional[str] = None
    end_date_sale: Optional[str] = None
    compatibility: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    developer: Optional[str] = None
    publisher: Optional[str] = None
    image: Optional[str] = None
    pass_product_id: Optional[str] = None
    release_date: Optional[str] = None
    capabilities: Optional[str] = None
    categories: Optional[str] = None
    videos: Optional[str] = None
    screenshots: Optional[str] = None
    size: Optional[int] = None
    voice_acting: Optional[str] = None
    interface_ru: Optional[str] = None
    subtitles: Optional[str] = None
    sale_product: Optional[int] = None
    dlc: Optional[str] = None
    prices: Optional[PricesSchema] = None

    @classmethod
    def from_db(cls, game: dict) -> "ProductResponse":
        return cls(
            id=game["id"],
            product_id=game["product_id"],
            url_product=game.get("url_product", ""),
            title=game.get("game_name", ""),
            end_date_sale=game.get("end_date_sale", ""),
            compatibility=game.get("device", ""),
            description=game.get("description", ""),
            short_description=game.get("short_description", ""),
            developer=game.get("developer_name", ""),
            publisher=game.get("publisher_name", ""),
            image=game.get("image_url", ""),
            pass_product_id=game.get("pass_product_id", ""),
            release_date=game.get("release_date", ""),
            capabilities=game.get("capabilities", ""),
            categories=game.get("category", ""),
            videos=game.get("link_video"),
            screenshots=game.get("link_screenshot", ""),
            size=game.get("game_weight", 0),
            voice_acting="russian" if game.get("audio_ru", 0) else "",
            interface_ru="russian" if game.get("interface_ru", 0) else "",
            subtitles="russian" if game.get("subtitles_ru", 0) else "",
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
