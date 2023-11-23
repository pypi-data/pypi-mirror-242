from django.urls import path, include
from rest_framework import routers

from modules.appeals_pos.api import AppealApi, CategoryApi, SettingsApi, FileAPI

router = routers.DefaultRouter()

router.register("file", FileAPI, basename="file")
router.register("appeals", AppealApi, basename="appeals")
router.register("categories", CategoryApi, basename="categories")
router.register("settings", SettingsApi, basename="settings")

urlpatterns = [
    path("", include(router.urls), name="api"),
]
