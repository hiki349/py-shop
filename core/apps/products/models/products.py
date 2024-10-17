from django.db import models

from core.apps.common.models import TimedBaseModel

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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
