from django.contrib import admin

from modules.core.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "feedback_user_full_name",
        "piece_of_comment",
    )
    fields = [
        "first_name",
        "last_name",
        "patronymic_name",
        "email",
        "phone",
        "comment",
    ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def piece_of_comment(self, obj):
        return obj.piece_of_comment

    def feedback_user_full_name(self, obj):
        return obj.full_name

    feedback_user_full_name.short_description = "ФИО"
    piece_of_comment.short_description = "Отзыв"
