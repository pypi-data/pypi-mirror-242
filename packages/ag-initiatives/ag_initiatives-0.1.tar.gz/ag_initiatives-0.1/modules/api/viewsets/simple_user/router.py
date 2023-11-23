from rest_framework import routers

from .initiative import InitiativeSimpleUserAPI
from .simple_user_info import SimpleUserInfoAPI

router = routers.SimpleRouter()

router.register("initiatives", InitiativeSimpleUserAPI, basename="simple_user_initiatives")

router.register("info", SimpleUserInfoAPI, basename="simple_user_info")
