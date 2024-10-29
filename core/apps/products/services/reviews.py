from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import ProductReviewEntity as ReviewEntity
from core.apps.products.exceptions.reviews import (
    ReviewInvalidRating,
    SingleReviewException,
)
from core.apps.products.models.reviews import ProductReview as ProductReviewModel


class BaseReviewService(ABC):
    @abstractmethod
    def check_review_exists(
        self,
        customer: CustomerEntity,
        product: ProductEntity,
    ) -> bool:
        ...

    @abstractmethod
    def save_review(
        self,
        product: ProductEntity,
        customer: CustomerEntity,
        review: ReviewEntity,
    ) -> ReviewEntity:
        ...


class ORMReviewService(BaseReviewService):
    def check_review_exists(
        self,
        customer: CustomerEntity,
        product: ProductEntity,
    ) -> bool:
        return ProductReviewModel.objects.filter(
            product_id=product.id,
            customer_id=customer.id,
        ).exists()

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


class SingleReviewValidatorService(BaseReviewValidatorService):
    service: BaseReviewService

    def validate(
        self,
        customer: CustomerEntity,
        product: ProductEntity,
        *args,
        **kwargs,
    ):
        if self.service.check_review_exists(customer=customer, product=product):
            raise SingleReviewException(product_id=product.id, customer_id=customer.id)


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
