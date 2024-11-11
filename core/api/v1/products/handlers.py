from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError

from core.api.filters import PaginationIn
from core.api.schemas import (
    ApiResponse,
    ListPagintedResponse,
    PaginationOut,
)
from core.api.v1.products.filters import ProductFilters
from core.api.v1.products.schemas import ProductSchema
from core.apps.common.exceptions import ServicesException
from core.apps.products.filters.products import ProductFilters as ProductFiltersEntity
from core.apps.products.services.products import BaseProductService
from core.project.containers import get_container


router = Router(tags=["Products"])


@router.get("", response=ApiResponse[ListPagintedResponse[ProductSchema]])
def get_product_list_handler(
    request: HttpRequest,
    filters: Query[ProductFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPagintedResponse[ProductSchema]]:
    container = get_container()
    service: BaseProductService = container.resolve(BaseProductService)

    product_list = service.get_product_list(
        filters=ProductFiltersEntity(search=filters.search),
        pagination=pagination_in,
    )
    product_count = service.get_product_count(filters=filters)

    items = [ProductSchema.from_entity(product) for product in product_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=product_count,
    )

    return ApiResponse(
        data=ListPagintedResponse(items=items, pagination=pagination_out),
    )


@router.get("{product_id}", response=ApiResponse[ProductSchema])
def get_product_by_id_handler(
    request: HttpRequest,
    product_id: int,
) -> ApiResponse[ProductSchema]:
    container = get_container()
    service: BaseProductService = container.resolve(BaseProductService)

    try:
        product = service.get_product_by_id(product_id)
    except ServicesException as exception:
        raise HttpError(
            status_code=404,
            message=exception.message,
        ) from exception

    return ApiResponse(data=ProductSchema.from_entity(product))
