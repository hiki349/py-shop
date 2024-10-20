from django.db import models

from core.apps.common.models import TimedBaseModel
from core.apps.products.entities.products import Product as ProductEntity

class Product(TimedBaseModel):
    title = models.CharField(
        verbose_name='Product title',
        max_length=255,
    )
    description = models.TextField(
        verbose_name='Product description',
        blank=True,
    )
    is_visible = models.BooleanField(
        verbose_name='Is product visible',
        default=True,
	)

    def to_entity(self) -> ProductEntity:
        return ProductEntity(
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
