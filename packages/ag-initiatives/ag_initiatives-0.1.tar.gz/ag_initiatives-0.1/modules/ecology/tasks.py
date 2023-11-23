from django.db.models import Q

from config.settings.celery import app
from django.utils import timezone
from modules.ecology.models import Event, GoodsNServicesItem
from modules.ecology.services import mail


@app.task(name="modules.ecology.tasks.publish_events")
def publish_events():
    current_date = timezone.localtime(timezone.now()).date()
    events_to_publish = Event.objects.filter(
        Q(
            start_publication_date__lte=current_date,
            expiry_publication_date__gte=current_date,
        )
        | Q(
            start_publication_date__lte=current_date,
            expiry_publication_date__isnull=True,
        )
    )
    events_to_unpublish = Event.objects.filter(
        start_publication_date__gt=current_date
    ) | Event.objects.filter(expiry_publication_date__lt=current_date)
    events_to_publish.update(is_published=True)
    events_to_unpublish.update(is_published=False)


@app.task(name="modules.ecology.tasks.publish_items")
def publish_items():
    current_date = timezone.localtime(timezone.now()).date()
    items_to_publish = GoodsNServicesItem.objects.filter(
        Q(
            start_publication_date__lte=current_date,
            expiry_publication_date__gte=current_date,
        )
        | Q(
            start_publication_date__lte=current_date,
            expiry_publication_date__isnull=True,
        )
    )
    items_to_unpublish = GoodsNServicesItem.objects.filter(
        start_publication_date__gt=current_date
    ) | GoodsNServicesItem.objects.filter(expiry_publication_date__lt=current_date)
    items_to_publish.update(is_published=True)
    items_to_unpublish.update(is_published=False)


@app.task
def send_email_on_participation_event(to, event_name, reward, from_email=None):
    mail.send_email_on_participation_event(to, event_name, reward, from_email)


@app.task
def send_email_on_purchase_confirm(to, reward_name, cost, from_email=None):
    mail.send_email_on_purchase_confirm(to, reward_name, cost, from_email)


@app.task
def send_email_on_participation_vote(to, vote_name, reward, from_email=None):
    mail.send_email_on_participation_vote(to, vote_name, reward, from_email)


@app.task
def send_email_on_user_adding_initiative(to, initiative_name, reward, from_email=None):
    mail.send_email_on_user_adding_initiative(to, initiative_name, reward, from_email)


@app.task
def send_email_on_user_approve_initiative(to, initiative_name, reward, from_email=None):
    mail.send_email_on_user_approve_initiative(to, initiative_name, reward, from_email)


@app.task
def send_email_on_ecology_participation(to, reward, from_email=None):
    mail.send_email_on_ecology_participation(to, reward, from_email)
