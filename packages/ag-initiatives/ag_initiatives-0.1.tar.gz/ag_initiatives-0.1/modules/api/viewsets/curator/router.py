from rest_framework import routers

from modules.api.viewsets.curator.curator_info import CuratorInfoAPI
from modules.api.viewsets.curator.department import DepartmentsCuratorAPI
from modules.api.viewsets.curator.initiative import CuratorInitiativeApi
from modules.api.viewsets.curator.initiative_accepting_settings import \
    CuratorInitiativeSettingsAPI
from modules.api.viewsets.curator.map_works import CuratorMapWorksApi
from modules.api.viewsets.curator.plans import CuratorPlansApi
from modules.api.viewsets.curator.user_manager import UserManagerApi
from modules.api.viewsets.curator.voting import CuratorVotingApi

router = routers.SimpleRouter()

router.register(
    "department",
    DepartmentsCuratorAPI,
    basename="curator_department"
)
router.register(
    "users",
    UserManagerApi,
    basename="curator_users_manager"
)
router.register(
    "voting",
    CuratorVotingApi,
    basename="curator_vote"
)
router.register(
    "initiative",
    CuratorInitiativeApi,
    basename="curator_initiative"
)
router.register(
    "initiative-settings",
    CuratorInitiativeSettingsAPI,
    basename="curator_initiative_settings"
)
router.register(
    "plans",
    CuratorPlansApi,
    basename="curator_plans"
)
router.register(
    "map-works",
    CuratorMapWorksApi,
    basename="curator_map_works"
)
router.register(
    "info",
    CuratorInfoAPI,
    basename="curator_info"
)
