from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

CELERY_BACKEND = ["amqp", "redis"][
    "redis" in os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
]

app = Celery("config", backend=CELERY_BACKEND)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update_vote_status": {
        "task": "modules.voting.services.mail_service.update_votes_status",
        "schedule": 60.0,
    },
    'update_vote_status_schedule': {
        'task': 'modules.initiatives.tasks.end_votes_collection_schedule',
        'schedule': 60.0,
    },
    "publish_events": {
        "task": "modules.ecology.tasks.publish_events",
        "schedule": 60.0,
    },
    "publish_items": {
        "task": "modules.ecology.tasks.publish_items",
        "schedule": 60.0,
    },
    "send_appeals_task": {
        "task": "modules.appeals_pos.tasks.send_appeals_task",
        "schedule": 30.0,
    },
    "send_file_task": {
        "task": "modules.appeals_pos.tasks.send_file_task",
        "schedule": 420.0,
    },
    "get_response_from_queue_task": {
        "task": "modules.appeals_pos.tasks.get_response_from_queue_task",
        "schedule": 30.0,
    },
    "update_pos_info": {
        "task": "modules.appeals_pos.tasks.update_pos_info",
        "schedule": 300.0,
    },

    # TODO: Необходимо изменить crontab(minute='*') на crontab(minute=0, hour=0) до 23.08.2023
    'deactivate_users': {
        'task': 'modules.core.tasks.deactivate_users',
        'schedule': crontab(minute='*'),
    },
}
app.conf.timezone = "Asia/Krasnoyarsk"

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
CELERY_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
