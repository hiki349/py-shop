from dataclasses import dataclass

from core.apps.common.exceptions import ServicesException


@dataclass(eq=False)
class ProductNotFound(ServicesException):
    product_id: int

    @property
    def message(self):
        return f'Product with id {self.product_id} was not found.'
