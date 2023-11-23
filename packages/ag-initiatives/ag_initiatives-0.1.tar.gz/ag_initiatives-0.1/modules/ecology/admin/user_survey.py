from django.contrib import admin

from modules.ecology.models import UserSurvey


@admin.register(UserSurvey)
class UserSurveyAdmin(admin.ModelAdmin):
    list_display = [
        "esia_id",
        "survey",
        "question",
        "answer",
    ]

    exclude = [
        "user",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def esia_id(self, instance):
        return instance.user.esia_id
