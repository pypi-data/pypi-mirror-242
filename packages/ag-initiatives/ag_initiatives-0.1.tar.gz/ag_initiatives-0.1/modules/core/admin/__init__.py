from .active_citizen_module_admin import ActiveCitizenModuleAdmin

# from .banner import BannerAdmin
from .department import DepartmentAdmin, LkoLevelAdmin, LkoTypeAdmin
from .locality import LocalityAdmin
from .news import NewsAdmin
from .user import UserAdmin
from .feedback import FeedbackAdmin

from django.contrib import admin
from rest_framework.authtoken.models import Token

from config.settings import settings

from .file import FileAdmin
# from .organization import OrganizationAdmin

from .video import VideoAdminInline
from .image import ImageAdminInline

# from .role_instruction import RoleInstructionAdmin
from .main_page_block import MainPageBlockAdmin
# from .lko_voting_description import LkoVotingDescriptionAdmin
# from .lko_initiative_description import LkoInitiativeDescriptionAdmin

from .user_action_tracking_admin import UserActionTrackingAdmin

if settings.DEBUG:
    admin.site.unregister(Token)

    @admin.register(Token)
    class CustomTokenAdmin(admin.ModelAdmin):
        list_display = ["key", "user", "created"]
        fields = ["user"]
        ordering = ["-created"]
        search_fields = ["user__last_name"]
        raw_id_fields = ["user"]


if settings.INVENTORY_STANDALONE:
    # admin.site.unregister(banner.Banner)
    admin.site.unregister(news.News)
    admin.site.unregister(feedback.Feedback)
    admin.site.unregister(project_info.ProjectInfo)
    admin.site.unregister(file.File)

# from .settings import SettingsAdmin

from .permissions_test import OperatorLkoPermissionsAdmin
from .categories_citizens import CategoryCitizenAdmin
from .settings_module import SettingsModuleAdmin
from .informational_messages import InformationalMessagesAdmin
from .deletion_notification import DeletionNotificationAdmin
