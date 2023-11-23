from django.urls import path, include
from rest_framework import routers

from modules.plans.api import (
    CategoryAPI,
    FileAPI,
    PlanAPI,
    PlanOperatorAPI,
    PlanUserAPI,
    PlanModeratorAPI,
    PlanCommentModeratorAPI,
)

router = routers.DefaultRouter()

router.register("category", CategoryAPI, basename="category")
router.register("file", FileAPI, basename="file")
router.register("plan", PlanAPI, basename="plan")
router.register("plan-operator", PlanOperatorAPI, basename="plan-operator")
router.register("plan-user", PlanUserAPI, basename="plan-user")
router.register("plan-moderator", PlanModeratorAPI, basename="plan-moderator")
router.register(
    "plan-comment-moderator", PlanCommentModeratorAPI, basename="plan-comment-moderator"
)

urlpatterns = [
    path("", include(router.urls), name="api"),
]
