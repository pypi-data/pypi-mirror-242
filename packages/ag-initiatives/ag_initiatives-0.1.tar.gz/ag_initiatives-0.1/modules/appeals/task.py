from django.core.mail import send_mail, EmailMessage

from config.settings.celery import app


@app.task
def send_email_on_appeal_state_change(subject, from_email, to, body, files=None):
    msg = EmailMessage(
        subject=subject,
        from_email=from_email,
        to=to,
        body=body,
    )

    if files is not None:
        for file in files:
            msg.attach_file(file)

    msg.send(fail_silently=True)

    return None
