from django.contrib import admin

from modules.voting.models import ImportXlsModel


@admin.register(ImportXlsModel)
class ImportXlsAdmin(admin.ModelAdmin):
    pass
