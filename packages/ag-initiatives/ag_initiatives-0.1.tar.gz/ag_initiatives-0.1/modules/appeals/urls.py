from django.urls import path, include
from rest_framework import routers

from modules.appeals.api import (
    AppealAPI,
    CategoryAPI,
    FileAPI,
    AppealUserAPI,
    AppealModeratorAPI,
    AppealOperatorAPI,
)

router = routers.DefaultRouter()

router.register("appeal", AppealAPI, basename="appeal")
router.register("appeal-user", AppealUserAPI, basename="appeal-user")
router.register("appeal-moderator", AppealModeratorAPI, basename="appeal-moderator")
router.register("appeal-operator", AppealOperatorAPI, basename="appeal-operator")
router.register("category", CategoryAPI, basename="category")
router.register("file", FileAPI, basename="file")

urlpatterns = [
    path("", include(router.urls), name="api"),
]
