from rest_framework import routers

from .initiative import InitiativeOperatorAPI
from .operator_info import OperatorInfoAPI

router = routers.SimpleRouter()

router.register("initiatives", InitiativeOperatorAPI, basename="operator_initiatives")

router.register("info", OperatorInfoAPI, basename="operator_info")
