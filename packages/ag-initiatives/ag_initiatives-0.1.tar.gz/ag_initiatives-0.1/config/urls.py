import debug_toolbar

from des import urls as des_urls
from des.models import DynamicEmailConfiguration
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django_summernote.models import Attachment
from rest_framework import permissions
from rest_framework.authtoken.models import Token

urlpatterns = [
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(settings.ADMIN_URL + "/", admin.site.urls),
    path("api/", include("modules.api.urls")),
    path("api/voting/", include("modules.voting.urls")),
    path("api/appeals/", include("modules.appeals.urls")),
    path("api/ecology/", include("modules.ecology.urls")),
    path("api/appeals-pos/", include("modules.appeals_pos.urls")),
    path("api/works-map/", include("modules.map_works.urls")),
    path("api/plans/", include("modules.plans.urls")),
    path("api/subscriptions/", include("modules.subscriptions.urls")),
    path("api/esia/", include("modules.esia.urls")),
    path("api/e-card/", include("modules.integration.urls")),
    path("nested_admin/", include("nested_admin.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("django-des/", include(des_urls)),
    url(r"^api/opinion/", include("modules.feedback.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Активный гражданин",
            default_version="v1",
            description="Документация API Активного гражданина",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
    ]

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )


if not settings.DEBUG:
    admin.site.unregister(Token)
admin.site.unregister(Attachment)

if settings.INVENTORY_STANDALONE:
    admin.site.unregister(DynamicEmailConfiguration)
