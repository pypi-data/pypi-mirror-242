from django.core.mail import EmailMessage

from config.settings.celery import app


@app.task
def send_email_on_vote_state_change(subject, from_email, to, body, files=None):
    html_body = body.replace("\n", "<br>") + '<br><br><img src="https://24ag.ru/media/logo2.png" alt="Изображение">'
    msg = EmailMessage(
        subject=subject,
        from_email=from_email,
        to=to,
        body=html_body,
    )

    if files is not None:
        for file in files:
            msg.attach_file(file)

    msg.content_subtype = 'html'
    msg.send(fail_silently=True)

    return None

@app.task
def send_email_on_local_vote_created(subject, from_email, to, body):
    msg = EmailMessage(
        subject=subject,
        from_email=from_email,
        to=to,
        body=body,
    )
    msg.send(fail_silently=True)

    return None
