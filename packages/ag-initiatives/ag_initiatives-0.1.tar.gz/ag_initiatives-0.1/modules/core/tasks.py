import uuid
from datetime import timedelta, datetime

from django.core.mail import send_mail
from django.utils import timezone

from config.settings.celery import app
from modules.core.models import User, UserRole


@app.task
def send_mail_with_with_feedback(data, receiver_email, from_email):
    send_mail(
        f'{data["first_name"]} {data["last_name"]} {data["patronymic_name"]} {data["phone"]} {data["email"]}',
        data["comment"],
        from_email,
        [receiver_email],
        fail_silently=False,
    )


@app.task
def deactivate_users():
    # TODO: Необходимо изменить timedelta(minutes=3) на timedelta(days=3) до 23.08.2023
    users_to_update = User.objects.filter(is_active=True, deletion_date__isnull=False)
    time_zone = timezone.get_current_timezone()
    for user in users_to_update:
        if user.deletion_date <= datetime.now().astimezone(time_zone) - timedelta(minutes=3):
            user.is_active = False
            user.deletion_date = None
            user.snils = None
            user.username = uuid.uuid4()
            user.roles = [UserRole.USER]
        user.save()
