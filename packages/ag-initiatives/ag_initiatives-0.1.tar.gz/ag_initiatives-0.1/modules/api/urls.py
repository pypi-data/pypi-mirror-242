from django.urls import path
from rest_framework import routers
from django.conf.urls import include

from modules.api.views.get_allowed_localities import get_allowed_localities, get_allowed_categories
from modules.api.views.import_permissions_from_excel import import_permissions_from_excel
from modules.api.viewsets import BackgroundTaskApi, AudioApi, UserArchivingAPI, LkoLevelAPI, LkoTypeAPI, \
    LocalityTypeAPI, InformationalMessagesAPI, DeletionNotificationAPI
from modules.api.viewsets.fias import FIASViewset
from modules.api.viewsets.operator_lko import router as operator_lko_router
from modules.api.viewsets.operator import router as operator_router
from modules.api.viewsets.moderator import router as moderator_router
from modules.api.viewsets.simple_user import router as simple_user_router

from modules.api.viewsets.admin_lko import router as admin_lko_router
from modules.api.viewsets.curator import router as curator_router
from modules.api.views import user_info, logout, stats, localities_categories
from modules.api.viewsets import (
    LocalityAPI,
    CategoryAPI,
    VoteAPI,
    VoteMunicipalAPI,
    VoteRegionalAPI,
    VoteLocalAPI,
    FeedbackViewSet,
    InitiativeCategoryAPI,
    InitiativeAPI,
    UserProfileAPI,
    InitiativeFileAPI,
    InitiativeSettingsAPI,
    InitiativeAcceptingSettingsViewSet,
    InitiativeCommunicationViewSet,
    ProjectInfoSerializerAPI,
    FileAPI,
    VideoApi,
    SettingsApi,
    ActiveCitizenModuleViewset,
    RoleInstructionViewSet,
    MainPageBlockAPI,
    DepartmentAPI,
    CategoryCitizenAPI,
    UploadingUsersAPI,
    DepartmentArchivingAPI,
    SettingsModuleAPI,
)
from modules.api.viewsets import NewsViewSet
from modules.api.viewsets.banner import BannerViewSet
from modules.api.viewsets.initiative_private import InitiativePrivateAPI
from modules.api.viewsets.initiative_reject_reason import InitiativeRejectReasonViewSet

router = routers.SimpleRouter()

router.register("locality", LocalityAPI, basename="locality")
router.register("vote_category", CategoryAPI, basename="vote_category")
router.register("vote", VoteAPI, basename="vote")
router.register("vote_municipal_user", VoteMunicipalAPI, basename="vote_municipal_user")
router.register("vote_regional_user", VoteRegionalAPI, basename="vote_regional_user")
router.register("vote_local_user", VoteLocalAPI, basename="vote_local_user")
router.register("news", NewsViewSet, basename="news")
router.register("banners", BannerViewSet, basename="banners")
router.register("feedback", FeedbackViewSet, basename="feedback")
router.register("fias", FIASViewset, basename="fias"),

router.register("role_instruction", RoleInstructionViewSet, basename="role_instruction")
router.register("main_page_block", MainPageBlockAPI, basename="main_page_block")

# router.register('opinion', FeedbackViewset, basename='opinion')

router.register("project-info", ProjectInfoSerializerAPI, basename="project-info")
router.register("file", FileAPI, basename="file")

router.register(
    "initiative-category", InitiativeCategoryAPI, basename="initiative-category"
)
router.register("initiative", InitiativeAPI, basename="initiative")
router.register(
    "initiative-private", InitiativePrivateAPI, basename="initiative-private"
)
router.register("initiative-file", InitiativeFileAPI, basename="initiative-file")
router.register(
    "initiative-settings", InitiativeSettingsAPI, basename="initiative-settings"
)
router.register(
    "initiative-accepting-settings",
    InitiativeAcceptingSettingsViewSet,
    basename="initiative-accepting-settings",
)
router.register(
    "initiatives-reject-reasons",
    InitiativeRejectReasonViewSet,
    basename="initiatives-reject-reasons",
)
router.register(
    "initiatives-communications",
    InitiativeCommunicationViewSet,
    basename="initiatives-communications",
)

router.register("user-profile", UserProfileAPI, basename="user-profile")
router.register("uploading-users", UploadingUsersAPI, basename="uploading-users")
router.register("user-archiving", UserArchivingAPI, basename="user-archiving")

router.register("video", VideoApi, basename="video")
router.register("audio", AudioApi, basename="audio")
router.register("core/settings", SettingsApi, basename="settings")
router.register("core/modules", ActiveCitizenModuleViewset, basename="modules")
router.register("department", DepartmentAPI, basename="department")
router.register("department-archiving", DepartmentArchivingAPI, basename="department-archiving")

router.register("background-task", BackgroundTaskApi, basename="background-task")
router.register("category-citizen", CategoryCitizenAPI, basename="category-citizen")

router.register("settings-module", SettingsModuleAPI, basename="instruction")

router.register("lko-level/dicts", LkoLevelAPI, basename="lko-levels")
router.register("lko-type/dicts", LkoTypeAPI, basename="lko-types")

router.register("localities_categories", LocalityTypeAPI, basename="localities_categories")

router.register("informational-messages", InformationalMessagesAPI, basename="informational_messages")
router.register("deletion-notification", DeletionNotificationAPI, basename="deletion-notification")

urlpatterns = [
    path("", include(router.urls), name="api"),
    path("curator/", include(curator_router.urls), name="curator"),
    path("admin-lko/", include(admin_lko_router.urls), name="admin_lko"),
    path("user_info", user_info, name="user_info"),
    path("logout", logout, name="logout"),
    path("stats", stats, name="stats"),
    path("operator-lko/", include(operator_lko_router.urls), name="operator_lko"),
    path("operator/", include(operator_router.urls), name="operator"),
    path("moderator/", include(moderator_router.urls), name="moderator"),
    path("simple-user/", include(simple_user_router.urls), name="simple_user"),
    path("get_allowed_localities", get_allowed_localities, name="get_allowed_localities"),
    path("get_allowed_categories", get_allowed_categories, name="get_allowed_categories"),
    path("import_permissions_from_excel", import_permissions_from_excel, name="import_permissions_from_excel"),
]
