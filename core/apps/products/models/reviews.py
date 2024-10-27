from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.customers.entities import CustomerEntity
from core.apps.products.entities.products import Product as ProductEntity
from core.apps.products.entities.reviews import ProductReviewEntity


class ProductReview(TimedBaseModel):
    customer = models.ForeignKey(
        to='customers.Customer',
        verbose_name='Reviewer',
        related_name='product_reviews',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to='products.Product',
        verbose_name='Reviewed Product',
        related_name='product_reviews',
        on_delete=models.CASCADE,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Customer rating',
        default=1,
    )
    text = models.TextField(
        verbose_name='Review text',
        blank=True,
        default='',
    )

    @classmethod
    def from_entity(
        cls,
        review: ProductReviewEntity,
        product: ProductEntity,
        customer: CustomerEntity,
    ) -> 'ProductReview':
        return cls(
            pk=review.id,
            product_id=product.id,
            customer_id=customer.id,
            rating=review.rating,
            text=review.text,
        )

    def to_entity(self) -> ProductReviewEntity:
        return ProductReviewEntity(
            id=self.id,
            text=self.text,
            rating=self.rating,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        unique_together = (
            ('customer', 'product')
        )
