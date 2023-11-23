from django.urls import path, include
from rest_framework import routers

from modules.map_works.api import (
    ContractorAPI,
    InstitutionTypeAPI,
    WorkCategoryAPI,
    WorkReasonAPI,
    WorkTypeAPI,
    WorksAPI,
    WorksOperatorAPI,
    LocationOperatorAPI,
)

router = routers.DefaultRouter()

router.register("category", WorkCategoryAPI, basename="category")
router.register("reason", WorkReasonAPI, basename="reason")
router.register("institution-type", InstitutionTypeAPI, basename="institution-type")
router.register("work-type", WorkTypeAPI, basename="work-type")
router.register("contractor", ContractorAPI, basename="contractor")
router.register("works", WorksAPI, basename="works")
router.register("works-operator", WorksOperatorAPI, basename="works-operator")
router.register("location-operator", LocationOperatorAPI, basename="location-operator")

urlpatterns = [
    path("", include(router.urls), name="api"),
]
