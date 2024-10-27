from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import ProductReviewEntity as ReviewEntity
from core.apps.products.exceptions.reviews import ReviewInvalidRating
from core.apps.products.models.reviews import ProductReview as ProductReviewModel


class BaseReviewService(ABC):
    @abstractmethod
    def save_review(
        self,
        product: ProductEntity,
        customer: CustomerEntity,
        review: ReviewEntity,
    ) -> ReviewEntity:
        ...


class ORMReviewService(BaseReviewService):
    def save_review(
        self,
        review: ReviewEntity,
        product: ProductEntity,
        customer: CustomerEntity,
    ) -> ReviewEntity:
        review_dto: ProductReviewModel = ProductReviewModel.from_entity(
            review=review, product=product, customer=customer,
        )
        review_dto.save()

        return review_dto.to_entity()


class BaseReviewValidatorService(ABC):
    @abstractmethod
    def validate(
        self,
        review: ReviewEntity,
        customer: CustomerEntity | None = None,
        product: ProductEntity | None = None,
    ):
        ...


class ReviewRatingValidatorService(BaseReviewValidatorService):
    def validate(self, review: ReviewEntity, *args, **kwargs):
        if not (1 <= review.rating <= 5):
            raise ReviewInvalidRating(rating=review.rating)


@dataclass
class ComposedReviewValidatorService(BaseReviewValidatorService):
    validators: list[BaseReviewValidatorService]

    def validate(
        self,
        review: ReviewEntity,
        product: ProductEntity | None = None,
        customer: CustomerEntity | None = None,
    ):
        for validator in self.validators:
            validator.validate(review=review, product=product, customer=customer)
