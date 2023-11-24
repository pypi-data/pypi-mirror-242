from ModelMagicAPI.autoapi import AutoApiViewset, AutoApiSerializer
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

def generate_auto_api(model):
    # print(f"Model: {model}")
    # if model:
    #     print(f"Model Name: {model.__name__}")
    #     print(f"Model Meta: {model._meta}")
    # else:
    #     print("Model is None")
    class AutoApi(AutoApiViewset):
        serializer_class = type(f"{model.__name__}Serializer", (AutoApiSerializer,), {"Meta": type("Meta", (AutoApiSerializer.Meta,), {"model": model})})
        queryset = model.objects.all()

    return AutoApi

router = routers.DefaultRouter()

def auto_discover_and_create_apis(models):
    global router
    router = routers.DefaultRouter()
    for model in models:
        api_viewset = generate_auto_api(model=model)
        router.register(f'{model.__name__.lower()}s', api_viewset)
    return router

def generate_swagger_schema(title, version):
    schema_view = get_schema_view(
        openapi.Info(
            title=title,
            default_version=version,
            description="Auto-generated API",
            terms_of_service="https://www.yourapp.com/terms/",
            contact=openapi.Contact(email="contact@yourapp.com"),
            license=openapi.License(name="Your License"),
        ),
        public=True,
    )
    return schema_view