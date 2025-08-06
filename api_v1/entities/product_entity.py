from dataclasses import dataclass

from api_v1.entities.price_entity import PricesEntity


@dataclass
class ProductEntity:
    id: int
    product_id: str
    title: str | None
    url_product: str | None
    end_date_sale: str | None
    compatibility: str | None
    description: str | None
    short_description: str | None
    developer: str | None
    publisher: str | None
    image: str | None
    pass_product_id: str | None
    release_date: str | None
    capabilities: str | None
    categories: list | None
    videos: list | None
    screenshots: list | None
    size: int | None
    voice_acting: str | None
    interface_ru: str | None
    subtitles: str | None
    sale_product: int | None
    dlc: str | None
    prices: PricesEntity | None