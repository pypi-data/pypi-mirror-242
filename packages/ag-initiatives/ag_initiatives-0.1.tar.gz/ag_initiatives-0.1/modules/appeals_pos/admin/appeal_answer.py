from django.contrib import admin

from modules.appeals_pos.models import AppealAnswer, AppealAttachment


class AppealAttachmentInline(admin.StackedInline):
    model = AppealAttachment
    fields = ["file"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False




@admin.register(AppealAnswer)
class AppealAnswerAdmin(admin.ModelAdmin):
    list_display = ["appeal_pos_id", "self_info"]
    list_display_links = ["self_info"]
    fields = ("appeal_pos_id", "appeal_state_change", "answer_type", "comment", "reject_reason")
    readonly_fields = ("appeal_pos_id",)
    inlines = [AppealAttachmentInline]

    def appeal_pos_id(self, obj: AppealAnswer) -> int:
        return obj.appeal_state_change.appeal.pos_id

    def self_info(self, obj: AppealAnswer) -> str:
        return str(obj)

    appeal_pos_id.short_description = "ПОС id обращения"
    self_info.short_description = "Информация"
