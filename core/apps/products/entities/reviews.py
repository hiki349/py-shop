from dataclasses import (
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)

from core.apps.common.enums import EntityStatust
from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product


@dataclass
class ProductReviewEntity:
    id: int | None = field(default=None, kw_only=True) # noqa
    customer: CustomerEntity | EntityStatust = field(default=EntityStatust.NOT_LOADED)
    product: Product | EntityStatust = field(default=EntityStatust.NOT_LOADED)
    text: str = field(default='')
    rating: int = field(default=1)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = field(default=None)
