from django.contrib import admin
from django.urls import include, path
from .views import api_overview, create, get, update, delete
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="App1 API",
        default_version="v1",
        description="My App1 backend API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="myemail@mail.com"),
        license=openapi.License(name="My License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #path('', include(router.urls)),
    path("list", api_overview, name="api_overview"),
    path("create", create, name="create_item"),
    path("get/", get, name="get_item"),
    path("update", update, name="update_item"),
    path("delete", delete, name="delete_item"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="app1-schema-swagger-ui"),
]