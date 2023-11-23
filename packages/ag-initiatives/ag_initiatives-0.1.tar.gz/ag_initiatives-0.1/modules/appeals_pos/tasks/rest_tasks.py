from django.utils import timezone

from config.settings.celery import app
from modules.appeals_pos.models import Settings
from modules.appeals_pos.services.rest.update_pos_service import UpdatePosService

update_service = UpdatePosService()


# Таски от REST сервиса (сейчас не используются)

@app.task()
def update_categories():
    update_service.update_categories()


@app.task()
def update_subcategories():
    update_service.update_subcategories()


@app.task()
def update_appeals():
    update_service.update_appeals()


@app.task()
def update_pos_info():
    settings: Settings = Settings.load()

    if settings.update_time.replace(second=0, microsecond=0) != timezone.datetime \
            .now().time().replace(second=0, microsecond=0):
        return

    update_service.update_categories()
    update_service.update_subcategories()
    update_service.update_appeals()
