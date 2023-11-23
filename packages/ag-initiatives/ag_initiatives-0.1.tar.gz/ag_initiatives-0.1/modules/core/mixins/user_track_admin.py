from modules.core.services import TrackUser


class TrackUserMixin(object):
    @TrackUser(action=["create", "update"])
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    @TrackUser(action=["delete"])
    def delete_model(self, request, obj):
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)


class TrackUserApiMixin(object):
    @classmethod
    @TrackUser(action=["create", "update"])
    def create(cls, request, obj, form, change):
        return obj

    @classmethod
    @TrackUser(action=["delete"])
    def delete(cls, request, obj, form, change):
        return obj
