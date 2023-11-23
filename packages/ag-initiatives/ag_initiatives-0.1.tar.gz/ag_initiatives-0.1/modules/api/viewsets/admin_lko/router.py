from rest_framework import routers

from modules.api.viewsets.admin_lko.admin_lko_info import AdminLkoInfoAPI
from modules.api.viewsets.admin_lko.allowed_fields import AllowedFieldsAPI
from modules.api.viewsets.admin_lko.department import DepartmentsAdminLkoAPI
from modules.api.viewsets.admin_lko.user_manager import UserManagerApi
from modules.api.viewsets.admin_lko.mail_invite import MailInviteAPI

router = routers.SimpleRouter()

router.register("department", DepartmentsAdminLkoAPI, basename="admin_lko_department")
router.register("users", UserManagerApi, basename="admin_lko_users_manager")
router.register("invite", MailInviteAPI, basename="admin_lko_mail_invite")
router.register("allowed-fields-info", AllowedFieldsAPI, basename="allowed-fields-info")
router.register("info", AdminLkoInfoAPI, basename="admin_lko_info")
