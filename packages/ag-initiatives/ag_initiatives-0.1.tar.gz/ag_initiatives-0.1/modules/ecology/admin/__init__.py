from django.contrib import admin

from config.settings import INVENTORY_STANDALONE
from .event import EventAdmin
from .event_category import EventCategoryAdmin
from .goods_n_services_item import GoodsNServicesItemAdmin
from .goods_n_services_item_category import GoodsNServicesItemCategoryAdmin
from .user_balance_operation import UserBalanceOperationAdmin
from .user_profile import UserProfileAdmin
from .settings import SettingsAdmin
from .notification import NotificationAdmin
from .participation_user_event import ParticipationUserEventAdmin
from .user_purchase import UserPurchaseAdmin

from .survey import SurveyAdmin
from .user_survey import UserSurveyAdmin


if INVENTORY_STANDALONE:
    admin.site.unregister(event.Event)
    admin.site.unregister(event_category.EventCategory)
    admin.site.unregister(goods_n_services_item.GoodsNServicesItem)
    admin.site.unregister(goods_n_services_item_category.GoodsNServicesItemCategory)
    admin.site.unregister(user_balance_operation.UserBalanceOperation)
    admin.site.unregister(user_profile.UserProfile)
    admin.site.unregister(settings.Settings)
    admin.site.unregister(notification.Notification)
    admin.site.unregister(participation_user_event.ParticipationUserEvent)
    admin.site.unregister(user_purchase.UserPurchase)
    admin.site.unregister(survey.Survey)
    admin.site.unregister(user_survey.UserSurvey)
