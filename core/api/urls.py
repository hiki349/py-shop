from django.urls import path
from ninja import NinjaAPI

from core.api.schemas import PingResponseSchema
from core.api.v1.urls import router as v1_router


api = NinjaAPI()


@api.get("/ping", response=PingResponseSchema)
def ping(request):
    return PingResponseSchema(result=True)


api.add_router("v1/", v1_router)

urlpatterns = [
    path("", api.urls),
]
