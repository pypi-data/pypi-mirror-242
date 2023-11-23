from rest_framework import routers

from modules.api.viewsets.operator_lko.allowed_fields import AllowedFieldsAPI
from modules.api.viewsets.operator_lko.initiative import (
    InitiativeOperatorLkoAPI
)
from modules.api.viewsets.operator_lko.initiative_accepting_settings import (
    InitiativeSettingsOperatorLkoAPI
)
from modules.api.viewsets.operator_lko.map_works import MapWorksOperatorLkoAPI
from modules.api.viewsets.operator_lko.operator_info import OperatorLkoInfoAPI
from modules.api.viewsets.operator_lko.plans import PlanOperatorLkoAPI
from modules.api.viewsets.operator_lko.voting import VotingOperatorLkoAPI

router = routers.SimpleRouter()

router.register(
    "initiatives",
    InitiativeOperatorLkoAPI,
    basename="operator_lko_initiatives"
)
router.register(
    "initiative-settings",
    InitiativeSettingsOperatorLkoAPI,
    basename="operator_lko_initiative_settings"
)
router.register(
    "map-works",
    MapWorksOperatorLkoAPI,
    basename="operator_lko_map_works"
)
router.register(
    "voting",
    VotingOperatorLkoAPI,
    basename="operator_lko_voting"
)
router.register(
    "plans",
    PlanOperatorLkoAPI,
    basename="operator_lko_plans"
)
router.register(
    "info",
    OperatorLkoInfoAPI,
    basename="operator_lko_info"
)
router.register(
    "allowed-fields-info",
    AllowedFieldsAPI,
    basename="allowed-fields-info"
)
