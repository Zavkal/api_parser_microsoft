from dataclasses import dataclass


@dataclass
class PriceInfoEntity:
    country: str | None
    price: float | int | None
    discounted_percentage: float | None


@dataclass
class PricesEntity:
    full_price: float | None
    key: PriceInfoEntity
    u_acc: PriceInfoEntity
    new_acc: PriceInfoEntity


