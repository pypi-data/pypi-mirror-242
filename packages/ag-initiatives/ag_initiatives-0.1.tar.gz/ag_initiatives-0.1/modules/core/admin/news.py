from django.contrib import admin
from django_summernote import admin as summernote_admin

from modules.core.models import News
from modules.core.mixins import TrackUserMixin
from embed_video.admin import AdminVideoMixin


@admin.register(News)
class NewsAdmin(AdminVideoMixin, TrackUserMixin, summernote_admin.SummernoteModelAdmin):
    summernote_fields = ["description", "text"]
