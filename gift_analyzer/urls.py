from typing import Any

from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view


class APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = [f'http', f'https']
        return schema


def get_swagger() -> Any:
    swagger = get_schema_view(
        openapi.Info(
            title="Analyzer API",
            default_version='v1',
            contact=openapi.Contact(email="email"),
        ),
        public=True,
        generator_class=APISchemeGenerator
    )
    return swagger


schema_view = get_swagger()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('villagers.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]