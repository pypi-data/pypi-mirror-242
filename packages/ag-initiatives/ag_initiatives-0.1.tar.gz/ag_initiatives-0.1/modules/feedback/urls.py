from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.urls import path, re_path

from modules.core.models import Locality
from modules.ecology.models import GoodsNServicesItemCategory, EventCategory
from modules.feedback.api.v1.viewsets import ObjectTypeViewset
from modules.feedback.api.v1.viewsets import OpinionViewset
from modules.feedback.api.v1.viewsets import ProblematicViewset
from modules.feedback.api.v1.viewsets import FIASViewset
from modules.feedback.api.v1.viewsets import EmailViewset
from modules.feedback.api.v1.viewsets import ShortLinkViewset
from modules.feedback.api.v1.viewsets.autocomplete import OrganizationProblematicAutocomplete, \
    OrganizationLocalityAutocomplete, OrganizationEventCategoryAutocomplete, \
    OrganizationGoodsNServicesItemCategoryAutocomplete
from modules.feedback.models import Problematic

router = routers.DefaultRouter()
schema_view = get_schema_view(title="Strelkovskij API")

# router.register('opinion/your-opinion-creation', FeedbackViewset, basename='opinion_creation')
# router.register('opinion', FeedbackViewset, basename='opinion')
# router.register('opinion/your-opinion-creation', FeedbackViewset, basename='create')
# router.register('tasks/json', TasksViewset, base_name='tasks_request')


urlpatterns = [
    path("user-opinion/", OpinionViewset.as_view({"get": "user_list"})),
    path("user-opinion/<int:pk>/", OpinionViewset.as_view({"get": "user_retrieve"})),
    path("operator-opinion/", OpinionViewset.as_view({"get": "operator_list"})),
    path("operator-opinion/xls/", OpinionViewset.as_view({"get": "operator_list"})),
    path(
        "operator-opinion/<int:pk>/",
        OpinionViewset.as_view({"get": "operator_retrieve"}),
    ),
    path(
        "operator-opinion/<int:pk>/xls/",
        OpinionViewset.as_view({"get": "operator_retrieve"}),
    ),
    path(
        "user-opinion/add/", OpinionViewset.as_view({"post": "create", "put": "create"})
    ),
    path("file/", OpinionViewset.as_view({"post": "upload", "put": "upload"})),
    path("object_type/", ObjectTypeViewset.as_view({"get": "list"})),
    path("object_type/<int:pk>/", ObjectTypeViewset.as_view({"get": "retrieve"})),
    path("problematic/", ProblematicViewset.as_view({"get": "list"})),
    path("problematic/<int:pk>/", ProblematicViewset.as_view({"get": "retrieve"})),
    path("fias/", FIASViewset.as_view({"get": "list"})),
    path("url/", ShortLinkViewset.as_view({"get": "links"})),
    # path('email/', EmailViewset.as_view({'get': 'send_email'})),

    re_path(
        'organization-problematic-autocomplete/$',
        OrganizationProblematicAutocomplete.as_view(model=Problematic),
        name='organization_problematic_autocomplete'
    ),
    re_path(
        'organization-goodsnservicesitemcategory-autocomplete/$',
        OrganizationGoodsNServicesItemCategoryAutocomplete.as_view(model=GoodsNServicesItemCategory),
        name='organization_goodsnservicesitemcategory_autocomplete'
    ),
    re_path(
        'organization-eventcategory-autocomplete/$',
        OrganizationEventCategoryAutocomplete.as_view(model=EventCategory),
        name='organization_eventcategory_autocomplete'
    ),
    re_path(
        'organization-locality-autocomplete/$',
        OrganizationLocalityAutocomplete.as_view(model=Locality),
        name='organization_locality_autocomplete'
    ),
]

# urlpatterns = [
#     url(r'^', include(router.urls)),
#     # url(r'^opinion/<pk:int>', FeedbackViewset.as_view({'get': 'retrieve'}), name='opinion'),
#     # url(r'^opinion', FeedbackViewset.as_view({'get': 'list'}), name='opinion'),
#     # url(r'^opinion/your-opinion-creation', FeedbackViewset.as_view({'POST': 'create', 'put': 'create'}), name='opinion_create')
# ]
