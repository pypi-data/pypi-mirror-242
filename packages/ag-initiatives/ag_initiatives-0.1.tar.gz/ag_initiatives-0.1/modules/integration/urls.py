from django.urls import path, include
from rest_framework import routers
from modules.integration.api.check import CheckSystemAccessApi
from modules.integration.api.citizen_category import CitizenCategoryApi

from modules.integration.api.dicts import DictAPI
from modules.integration.api.event import EventAPI
from modules.integration.api.goodsnservicesitem import GoodsNServicesItemAPI
from modules.integration.api.initiative import InitiativeAPI
from modules.integration.api.user import UserAPI
from modules.integration.api.user_code import ExternalSystemEventApi, ExternalSystemGoodNServicesApi
from modules.integration.api.voting import VoteAPI

router = routers.DefaultRouter()

router.register("vote", VoteAPI, basename="vote")
router.register("initiative", InitiativeAPI, basename="initiative")
router.register("offers", EventAPI, basename="event")
router.register("rewards", GoodsNServicesItemAPI, basename="goodsnservicesitem")
router.register("users", UserAPI, basename="user")
router.register("citizen-category", CitizenCategoryApi, basename="citizen_category")

urlpatterns = [
    path("", include(router.urls), name="api"),
    path("users/<int:pk>/", UserAPI.as_view({'post': 'create_with_id'}), name='create_with_id'),
    path("dicts/", DictAPI.as_view(), name="dict"),
    path("check/", CheckSystemAccessApi.as_view(), name="access"),
    path("use_offer/", ExternalSystemEventApi.as_view(), name="use-offer"),
    path("use_reward/", ExternalSystemGoodNServicesApi.as_view(), name="use-reward"),

]
