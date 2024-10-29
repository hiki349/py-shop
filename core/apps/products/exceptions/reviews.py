from dataclasses import dataclass

from core.apps.common.exceptions import ServicesException


@dataclass(eq=False)
class ReviewInvalidRating(ServicesException):
    rating: int

    @property
    def message(self):
        return 'Rating is not valid.'


@dataclass(eq=False)
class SingleReviewException(ServicesException):
    product_id: int
    customer_id: int

    @property
    def message(self):
        return f'Customer with id {self.customer_id} already has a review for product with id {self.product_id}.'
