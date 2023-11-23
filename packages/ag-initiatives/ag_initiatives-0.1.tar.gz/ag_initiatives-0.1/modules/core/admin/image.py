from django.contrib import admin
from modules.core.models import Image


@admin.register(Image)
class ImageAdminInline(admin.ModelAdmin):
    pass
