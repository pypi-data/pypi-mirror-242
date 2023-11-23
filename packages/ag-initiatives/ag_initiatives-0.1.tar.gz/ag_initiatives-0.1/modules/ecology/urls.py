from django.urls import path, include
from rest_framework import routers

from modules.ecology.api import (
    EventCategoryAPI,
    GoodsNServicesItemCategoryAPI,
    EventAPI,
    FileAPI,
    UserProfileAPI,
    GoodsNServicesItemAPI,
    SettingsAPI,
    PartnerHistoryAPI,
)
from modules.ecology.api.organizer import OrganizerParticipationAPI
from modules.ecology.api.partner import PartnerPurchaseAPI, PartnerAPI
from modules.ecology.api.user_profile import UserParticipationAPI, UserPurchaseAPI

router = routers.DefaultRouter()

router.register("event-category", EventCategoryAPI, basename="event-category")
router.register(
    "goods-n-services-item-category",
    GoodsNServicesItemCategoryAPI,
    basename="goods-n-services-item-category",
)

router.register("event", EventAPI, basename="event")
router.register(
    "goods-n-services-item", GoodsNServicesItemAPI, basename="goods-n-services-item"
)

router.register("partner", PartnerAPI, basename="partner")
router.register("partner/history", PartnerHistoryAPI, basename="partner-history")
router.register(
    "partner/rewards-receive", PartnerPurchaseAPI, basename="partner-rewards-receive"
)

router.register(
    "organizer/participation",
    OrganizerParticipationAPI,
    basename="organizer-participation",
)

router.register("user-profile", UserProfileAPI, basename="user-profile")
router.register(
    "user/participation", UserParticipationAPI, basename="user-participation"
)
router.register("user/rewards-receive", UserPurchaseAPI, basename="user-purchase")

router.register("file", FileAPI, basename="file")

router.register("settings", SettingsAPI, basename="settings")

urlpatterns = [
    path("", include(router.urls), name="api"),
    # path('event-user/registration/<int:pk>', EventAPI.as_view({'get': 'registration'}))
]
