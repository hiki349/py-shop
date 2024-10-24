from dataclasses import (
    dataclass,
    field,
)

from core.apps.common.enums import EntityStatust
from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product


@dataclass
class ProductReviewEntity:
    customer: CustomerEntity | EntityStatust = field(default=EntityStatust.NOT_LOADED)
    product: Product | EntityStatust = field(default=EntityStatust.NOT_LOADED)
    text: str = field(default='')
    rating: int
