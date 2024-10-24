from django.db import models

from core.apps.common.models import TimedBaseModel


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

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        unique_together = (
            ('customer', 'product')
        )
