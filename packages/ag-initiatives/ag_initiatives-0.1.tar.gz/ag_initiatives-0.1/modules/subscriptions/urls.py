from django.urls import path, include
from rest_framework import routers

from modules.subscriptions.api import (
    SubscriptionAPI,
    EventEnumAPI,
    ActiveCitizenModuleEnumAPI,
    CategoryAPI,
    LocalityAPI,
    SubscriptionTemplateAPI,
)

router = routers.DefaultRouter()

router.register("subscription", SubscriptionAPI, basename="subscription")
router.register("event-enum", EventEnumAPI, basename="event-enum")
router.register("module-enum", ActiveCitizenModuleEnumAPI, basename="module-enum")
router.register("category-enum", CategoryAPI, basename="category-enum")
router.register("locality-enum", LocalityAPI, basename="locality-enum")
router.register("template-enum", SubscriptionTemplateAPI, basename="template-enum")
urlpatterns = [path("", include(router.urls), name="api")]
