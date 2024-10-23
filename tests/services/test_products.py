import pytest
from tests.factories.products import ProductModelFactory

from core.api.filters import PaginationIn
from core.api.v1.products.filters import ProductFilters
from core.apps.products.services.products import BaseProductService


@pytest.mark.django_db
def test_get_products_count_zero(product_service: BaseProductService):
    """
    Test product count zero with no products in database.
    """
    product_count = product_service.get_product_count(ProductFilters())
    assert product_count == 0, f'{product_count=}'


@pytest.mark.django_db
def test_get_products_count_exist(product_service: BaseProductService):
    """
    Test product count with products in database.
    """
    expected_count = 5
    ProductModelFactory.create_batch(size=expected_count)

    product_count = product_service.get_product_count(ProductFilters())
    assert product_count == expected_count, f'{product_count=}'


@pytest.mark.django_db
def test_get_products_all(product_service: BaseProductService):
    """
    Test product count with products in database.
    """
    expected_count = 5
    products = ProductModelFactory.create_batch(size=expected_count)
    products_titles = {product.title for product in products}

    fetched_products = product_service.get_product_list(
        ProductFilters(),
        PaginationIn(),
    )
    fetched_titles = {product.title for product in fetched_products}

    assert len(products_titles) == expected_count, f'{fetched_titles=}'
    assert products_titles == fetched_titles, f'{fetched_titles=}'


@pytest.mark.django_db
def test_get_products_zero(product_service: BaseProductService):
    """
    Test product count with zero products in database.
    """
    fetched_products = product_service.get_product_list(
        ProductFilters(),
        PaginationIn(),
    )
    assert len(fetched_products) == 0, f'{len(fetched_products)=}'
