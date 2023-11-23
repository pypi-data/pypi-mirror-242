import importlib
import random
from typing import Optional, Union, Dict

from django.db import IntegrityError
from django.db.models import QuerySet
from django.utils import timezone

from modules.core.models import User, Locality
from modules.subscriptions.enums import EventEnum, ActiveCitizenModuleEnum
from modules.subscriptions.models import SubscriptionTemplate, Subscription


class Common(object):

    _meta = None
    _model = None

    def __new__(cls, *args, **kwargs):
        result = super().__new__(cls)
        cls.subscription_data = cls.generate_subscription_data()
        return result

    @classmethod
    def generate_subscription_data(cls, event: str = None) -> Dict:
        event = random.choice(list(EventEnum.RESOLVER.keys()))
        module = cls.get_module(event)
        category = cls.get_category(module)
        subscription_data = {key: value for key, value in cls.subscription_data.items()}
        subscription_data["event"] = event
        subscription_data["module"] = module
        subscription_data["category"] = category

        return subscription_data

    @classmethod
    def _basic_setup(cls):
        locality = Locality.objects.create(**cls.locality_data)
        cls.user_data["residential_locality"] = locality
        cls.user_data["registration_locality"] = locality
        user = User.objects.create(**cls.user_data)
        for event_type, event_data in cls.subscriptions_template_data.items():
            subscription_template = SubscriptionTemplate.objects.create(**event_data)

    @classmethod
    def create_subscription_object(cls, event=None):
        if event:
            cls.generate_subscription_data(event)
            cls.subscription_data["event"] = event
        cls.subscription_data["user"] = User.objects.all().first()
        cls.subscription_data["locality"] = Locality.objects.all().first()
        cls.subscription_data["template"] = cls.get_template(
            cls.subscription_data["event"], SubscriptionTemplate.objects.all()
        )
        result = Subscription.objects.create(**cls.subscription_data)
        return result

    @classmethod
    def print_success(cls, obj):
        print(
            f">>> Object by model {obj.__class__.__name__} - {obj} ({obj.id}) was created!"
        )

    @classmethod
    def clear_tag_name(cls, tag_name):
        tag_name = tag_name.lstrip("<")
        tag_name = tag_name.lstrip("/")
        tag_name = tag_name.rstrip(">")
        tag_name = tag_name.split(" ")[0]
        return tag_name

    @classmethod
    def get_module(cls, event: str) -> Optional[str]:
        result = None
        if event in EventEnum.VOTING:
            result = ActiveCitizenModuleEnum.core
        if event in EventEnum.INITIATIVES:
            result = ActiveCitizenModuleEnum.initiatives
        if event in EventEnum.PLANS:
            result = ActiveCitizenModuleEnum.plans
        if event in EventEnum.MAP_WORKS:
            result = ActiveCitizenModuleEnum.ap_works
        if event in EventEnum.NEWS:
            result = ActiveCitizenModuleEnum.core
        return result

    @classmethod
    def get_template(
        cls, event: str, subscription_templates: Union[QuerySet, SubscriptionTemplate]
    ) -> Union[SubscriptionTemplate, QuerySet]:
        result = subscription_templates.none()
        if event in EventEnum.START_EVENT:
            result = subscription_templates.filter(event_type="START_EVENT").first()
        if event in EventEnum.PUBLISH_EVENT:
            result = subscription_templates.filter(event_type="PUBLISH_EVENT").first()
        if event in EventEnum.END_EVENT:
            result = subscription_templates.filter(event_type="END_EVENT").first()
        return result

    @classmethod
    def get_category(cls, module):
        result = ""
        if module == "ap_works":
            module = "m" + module
        models = importlib.import_module(f"modules.{module}.models")
        if module == "core":
            result = f"{module}:Category:1"
            models.Category.objects.create(name="Category")
        elif module == "initiatives":
            result = f"{module}:InitiativeCategory:1"
            models.InitiativeCategory.objects.create(name="InitiativeCategory")
        elif module == "map_works":
            result = f"{module}:WorkCategory:1"
            models.WorkCategory.objects.create(name="WorkCategory")
        elif module == "plans":
            result = "core:Category:1"
            models.Category.objects.create(name="Category")
        return result

    IntegrityError = IntegrityError

    subscription_data = {
        "user": None,
        "event": None,
        "category": None,
        "module": None,
        "template": None,
        "locality": None,
    }

    locality_data = {
        "name": "Красноярск",
        "type": 40,
    }
    user_data = {
        "first_name": "Кирилл",
        "last_name": "Стрелковский",
        "patronymic_name": "Константинович",
        "birth_date": timezone.datetime(1988, 12, 26).astimezone().date(),
        "email": "kstr88@mail.ru",
        "email_initiative_notification": True,
        "phone": "+79233066700",
        "roles": ["USER"],
        "residential_locality": None,
        "registration_locality": None,
        "esia_verified": True,
        "department": None,
        "organization": None,
    }
    subscriptions_template_data = {
        "start_event": {
            "title": 'Начало события "{event}" ',
            "body": '<h1>Доброго времени суток "{user}"!</h1><hr>'
            "<p>Вы получили это уведомление поскольку подписаны "
            'на начало события "<b>{event}</b>" категории '
            '"<b>{category}</b>" (<b>{locality}</b>). <br>Событие '
            '"<b>{event}</b>" началось <b>{date}</b>  в <b>{time}</b>!'
            "</p><hr><p></p><p><br></p><p><br><br></p><p></p>",
            "event_type": "START_EVENT",
        },
        "publish_event": {
            "title": 'Публикация события "{event}" ',
            "body": '<h1>Доброго времени суток "{user}"!</h1><hr>'
            "<p>Вы получили это уведомление поскольку подписаны "
            'на публикацию события "<b>{event}</b>" категории '
            '"<b>{category}</b>" (<b>{locality}</b>). <br>Событие '
            '"<b>{event}</b>" опубликовано <b>{date}</b>  в <b>{time}</b>!'
            "</p><hr><p></p><p><br></p><p><br></p><p></p><p></p><p><br><br></p><p></p>",
            "event_type": "PUBLISH_EVENT",
        },
        "end_event": {
            "title": 'Окончание события "{event}" ',
            "body": '<h1>Доброго времени суток "{user}"!</h1><hr>'
            "<p>Вы получили это уведомление поскольку подписаны "
            'на окончание события "<b>{event}</b>" категории '
            '"<b>{category}</b>" (<b>{locality}</b>). <br>Событие '
            '"<b>{event}</b>" закончилось <b>{date}</b>  в <b>{time}</b>!'
            "</p><hr><p></p><p><br></p><p><br></p><p></p><p></p><p><br><br></p><p></p>",
            "event_type": "END_EVENT",
        },
    }
    single_tags = (
        "area",
        "base",
        "basefont",
        "bgsound",
        "br",
        "col",
        "command",
        "embed",
        "hr",
        "img",
        "input",
        "isindex",
        "keygen",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    )


@classmethod
def none_func(cls):
    return QuerySet().none()


Objects = type(
    "Objects",
    (),
    {
        "all": none_func,
        "first": none_func,
        "last": none_func,
        "get": none_func,
        "filter": none_func,
    },
)


class ModelCommon(Common):
    class Meta:
        class Model:
            _meta = None
            objects = Objects()

        model = Model

    def __new__(cls, *args, **kwargs):
        result = super().__new__(cls)
        cls._model = cls.Meta.model
        cls._meta = cls._model._meta
        return result
