import os
from config.settings.celery import app
from des.models import DynamicEmailConfiguration

from django.core.mail import EmailMessage


@app.task
def send_email_on_appeal_state_change(subject, from_email, to, body, file_path=None):
    try:
        msg = EmailMessage(
            subject=subject,
            from_email=from_email,
            to=to,
            body=body,
        )
        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as file:
                name = os.path.basename(file_path)
                msg.attach(name, file.read())
        msg.send(fail_silently=True)
    except Exception as e:
        print(f"5. {e}")
        err = EmailMessage(
            subject="Ошибка",
            from_email=str(
                getattr(DynamicEmailConfiguration.get_solo(), "from_email", None)
            ),
            to=["strelkovskijkk@cifra-k.ru"],
            body=f"5. {e}",
        )
        err.send(fail_silently=False)

    return None
