from django.core.mail import send_mail
from config.settings.celery import app
from modules.initiatives.service.votes_collection import _end_votes_collection, _end_votes_collection_schedule


@app.task
def send_email_on_initiative_state_change(**kwargs):
    _send_mail_wrapper(**kwargs)


@app.task
def send_email_initiative_broadcast(**kwargs):
    _send_mail_broadcast_wrapper(**kwargs)


def _send_mail_wrapper(**kwargs):
    text = kwargs.get("text")
    html_text = text.replace("\n", "<br>") + '<br><br><img src="https://24ag.ru/media/logo2.png" alt="Изображение">'
    send_mail(
        message=text,
        subject=kwargs.get("subject"),
        html_message=html_text,
        from_email=kwargs.get("from_mail"),
        recipient_list=[kwargs.get("to_mail")],
        fail_silently=False,
    )


def _send_mail_broadcast_wrapper(**kwargs):
    text = kwargs.get("text")
    html_text = text.replace("\n", "<br>") + '<br><br><img src="https://24ag.ru/media/logo2.png" alt="Изображение">'
    send_mail(
        message=text,
        subject=kwargs.get("subject"),
        html_message=html_text,
        from_email=kwargs.get("from_mail"),
        recipient_list=kwargs.get("to_mail"),
        fail_silently=False,
    )


@app.task
def end_votes_collection(**kwargs):
    _end_votes_collection(pk=kwargs["pk"])


@app.task
def end_votes_collection_schedule(**kwargs):
    _end_votes_collection_schedule()
