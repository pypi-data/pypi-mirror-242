import importlib
import importlib.util
import random
from asyncio import sleep

from django.test import TestCase

from modules.core.models import Locality, User
from modules.subscriptions.enums import EventEnum, ActiveCitizenModuleEnum
from modules.subscriptions.models import (
    Subscription,
    SubscriptionTemplate,
    NotificationSendingLog,
)
from modules.subscriptions.tests.common_data_for_tests import ModelCommon


class SubscriptionTestCase(TestCase, ModelCommon):
    class Meta:
        model = Subscription

    @classmethod
    def setUpTestData(cls):
        cls._basic_setup()

    def setUp(self) -> None:
        self.create_subscription_object()

    def test_user_label(self):
        field_label = self._meta.get_field("user").verbose_name
        self.assertEqual(field_label, "Пользователь системы")

    def test_user_str(self):
        obj = self._model.objects.all().first()
        user = obj.user
        self.assertEqual(
            f"{user}",
            f'{self.user_data["first_name"]} {self.user_data["patronymic_name"]} {self.user_data["last_name"]}',
        )

    def test_user_null(self):
        obj = self._model.objects.all().first()
        obj.user = None
        with self.assertRaises(self.IntegrityError):
            obj.save()

    def test_user_related_name(self):
        subscriptions = self._model.objects.all()
        user = User.objects.all().first()
        user_subscriptions = user.subscriptions.all()
        self.assertEqual(user_subscriptions.count(), subscriptions.count())

    def test_locality_label(self):
        field_label = self._meta.get_field("locality").verbose_name
        self.assertEqual(field_label, "Населенный пункт")

    def test_locality_str(self):
        obj = self._model.objects.all().first()
        locality = obj.locality
        self.assertEqual(
            f"{locality}",
            f'{self.locality_data["name"]}',
        )

    def test_locality_null(self):
        obj = self._model.objects.all().first()
        obj.locality = None
        with self.assertRaises(self.IntegrityError):
            obj.save()

    def test_locality_related_name(self):
        subscriptions = self._model.objects.all()
        locality = Locality.objects.all().first()
        locality_subscriptions = locality.subscriptions.all()
        self.assertEqual(locality_subscriptions.count(), subscriptions.count())

    def test_event_label(self):
        field_label = self._meta.get_field("event").verbose_name
        self.assertEqual(field_label, "Событие")

    def test_event_display(self):
        obj = self._model.objects.all().first()
        self.assertEqual(obj.event_display, EventEnum.get(obj.event))

    def test_event_value(self):
        obj = self._model.objects.all().first()
        self.assertIn(obj.event, EventEnum.RESOLVER.keys())

    def test_event_length(self):
        field_length = self._meta.get_field("event").max_length
        self.assertEqual(field_length, 255)

    def test_module_label(self):
        field_label = self._meta.get_field("module").verbose_name
        self.assertEqual(field_label, "Модуль")

    def test_module_display(self):
        obj = self._model.objects.all().first()
        self.assertEqual(obj.module_display, ActiveCitizenModuleEnum.get(obj.module))

    def test_module_value(self):
        obj = self._model.objects.all().first()
        self.assertIn(obj.module, ActiveCitizenModuleEnum.RESOLVER.keys())

    def test_module_length(self):
        field_length = self._meta.get_field("module").max_length
        self.assertEqual(field_length, 255)

    def test_category_label(self):
        field_label = self._meta.get_field("category").verbose_name
        self.assertEqual(field_label, "Категория")

    def test_category_help_text(self):
        help_text = self._meta.get_field("category").help_text
        self.assertEqual(help_text, "модуль:Модель:pk")

    def test_category_value(self):
        obj = self._model.objects.all().first()
        category = obj.category
        module_name = category.split(":")[0]
        model_name = category.split(":")[1]
        model_object_pk = category.split(":")[-1]
        spec = importlib.util.find_spec(f"modules.{module_name}.models.{model_name}")
        category_object = None
        if spec:
            model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(model)
            category_object = model.objects.filter(pk=model_object_pk).first()
        if category_object:
            self.assertEqual(obj.category_value, category_object)
        else:
            self.assertEqual(obj.category_value, None)

    def test_category_display(self):
        obj = self._model.objects.all().first()
        category = obj.category
        module_name = category.split(":")[0]
        model_name = category.split(":")[1]
        model_object_pk = category.split(":")[-1]
        spec = importlib.util.find_spec(f"modules.{module_name}.models.{model_name}")
        category_object = None
        if spec:
            model = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(model)
            category_object = model.objects.filter(pk=model_object_pk).first()

        if category_object:
            self.assertEqual(obj.category_value, f"{category_object}")
        else:
            self.assertEqual(obj.category_value, None)

    def test_category_length(self):
        field_length = self._meta.get_field("category").max_length
        self.assertEqual(field_length, 255)

    def test_template_label(self):
        field_label = self._meta.get_field("template").verbose_name
        self.assertEqual(field_label, "Шаблон письма")

    def test_template_related_name(self):
        subscriptions = self._model.objects.all().first()
        template = subscriptions.template
        templates = SubscriptionTemplate.objects.filter(pk=template.pk)
        template_subscriptions = template.subscriptions.all()
        self.assertEqual(templates.count(), template_subscriptions.count())

    def test_model_str(self):
        obj = self._model.objects.first()
        user_str = (
            f'{self.user_data["first_name"]} '
            f'{self.user_data["patronymic_name"]} '
            f'{self.user_data["last_name"]}'
        )
        locality_str = f'{self.locality_data["name"]}'
        module_str = f'{ActiveCitizenModuleEnum.get(self.subscription_data["module"])}'
        event_str = f'{EventEnum.get(self.subscription_data["event"])}'
        category_str = f"{obj.category_value}"
        self.assertEqual(
            f"{obj}",
            f"{user_str}: "
            f"{locality_str}/"
            f"{module_str}/"
            f"{event_str}/"
            f"{category_str}/",
        )

    def test_model_verbose_name(self):
        self.assertEqual(self._meta.verbose_name, "Подписка пользователя")

    def test_model_verbose_name_plural(self):
        self.assertEqual(self._meta.verbose_name_plural, "Подписки пользователей")

    def test_model_unique_together(self):
        self.assertEqual(
            self._meta.unique_together, (("user", "event", "module", "template"),)
        )

    def test_unique_composite_key(self):
        obj = self._model.objects.first()
        with self.assertRaises(self.IntegrityError):
            new_obj = self.create_subscription_object()


class SubscriptionTemplateTestCase(TestCase, ModelCommon):
    class Meta:
        model = SubscriptionTemplate
        special_words = [
            "{event}",
            "{user}",
            "{category}",
            "{locality}",
            "{date}",
            "{time}",
        ]

    @classmethod
    def setUpTestData(cls):
        cls._basic_setup()

    def setUp(self) -> None:
        for event_type, event_data in self.subscriptions_template_data.items():
            subscription_template = self._model.objects.create(**event_data)

    def test_title_label(self):
        verbose_name = self._meta.get_field("title").verbose_name
        self.assertEqual(verbose_name, "Заголовок")

    def test_title_help_text(self):
        verbose_name = self._meta.get_field("title").help_text
        self.assertEqual(
            verbose_name, "Для указания события используйте указатель `{event}`"
        )

    def test_title_max_length(self):
        verbose_name = self._meta.get_field("title").max_length
        self.assertEqual(verbose_name, 1000)

    def test_title_special_word(self):
        subscription_templates = self._model.objects.all().values("title")
        titles = [template.get("title") for template in subscription_templates]
        for title in titles:
            title_list = title.split("{")
            special_words = [item.split("}")[0] for item in title_list if "}" in item]
            for special_word in special_words:
                self.assertIn("{" + special_word + "}", self.Meta.special_words)

    def test_body_label(self):
        verbose_name = self._meta.get_field("body").verbose_name
        self.assertEqual(verbose_name, "Тело письма")

    def test_body_help_text(self):
        verbose_name = self._meta.get_field("body").help_text
        self.assertEqual(
            verbose_name,
            "Указатели: "
            "`{event}` - событие; "
            "`{user}` - ФИО пользователя; "
            "`{category}` - категория; "
            "`{locality}` - населённый пункт; "
            "`{date}` - дата события; "
            "`{time}` - время события",
        )

    def test_body_special_word(self):
        subscription_templates = self._model.objects.all().values("body")
        bodies = [template.get("body") for template in subscription_templates]
        for body in bodies:
            body_list = body.split("{")
            special_words = [item.split("}")[0] for item in body_list if "}" in item]
            for special_word in special_words:
                self.assertIn("{" + special_word + "}", self.Meta.special_words)

    def test_body_html_tags(self):
        subscription_templates = SubscriptionTemplate.objects.all().values("body")
        subscription_templates_body = [
            item.get("body") for item in subscription_templates
        ]

        for body_data in subscription_templates_body:
            tags = set()
            tag_flag = False
            tag_name = ""
            for sign in body_data:
                tag_name += ["", sign][tag_flag]
                if sign == "<":
                    tag_flag = True
                if sign == ">":
                    tag_flag = False
                    tags.add(self.clear_tag_name(tag_name))
                    tag_name = ""
            for tag in tags:
                if tag not in self.single_tags:
                    self.assertEqual(
                        body_data.count(f"<{tag} ") + body_data.count(f"<{tag}>"),
                        body_data.count(f"</{tag}>"),
                    )

    def test_event_type_label(self):
        verbose_name = self._meta.get_field("event_type").verbose_name
        self.assertEqual(verbose_name, "Тип события")

    def test_event_type_max_length(self):
        verbose_name = self._meta.get_field("event_type").max_length
        self.assertEqual(verbose_name, 255)

    def test_event_type_value(self):
        subscription_templates = self._model.objects.all().values("event_type")
        event_types = [
            template.get("event_type") for template in subscription_templates
        ]
        for event_type in event_types:
            self.assertIn(event_type, EventEnum.TYPE_RESOLVER.keys())

    def test_model_str(self):
        subscription_templates = self._model.objects.all()
        for template in subscription_templates:

            template_str = self.subscriptions_template_data[
                template.event_type.lower()
            ].get("title")

            self.assertEqual(f"{template}", template_str)

    def test_model_verbose_name(self):
        self.assertEqual(self._meta.verbose_name, "Шаблон письма")

    def test_model_verbose_name_plural(self):
        self.assertEqual(self._meta.verbose_name_plural, "Шаблоны писем")


class NotificationSendingLogTestCase(TestCase, ModelCommon):
    class Meta:
        model = NotificationSendingLog

    @classmethod
    def setUpTestData(cls):
        cls._basic_setup()
        subscription_count = 5
        events = set(
            [
                random.choice(list(EventEnum.RESOLVER.keys()))
                for _ in range(subscription_count)
            ]
        )
        while len(events) < subscription_count and len(events) <= len(
            EventEnum.RESOLVER
        ):

            events = set(
                [
                    random.choice(list(EventEnum.RESOLVER.keys()))
                    for _ in range(subscription_count)
                ]
            )
            if cls.subscription_data["event"] in events:
                events.remove(cls.subscription_data["event"])
        for event in events:
            cls.create_subscription_object(event)

    def setUp(self) -> None:
        subscriptions = Subscription.objects.all()
        status = True
        for subscription in subscriptions:
            self._model.objects.create(status=status, subscription=subscription)

    def test_timestamp_label(self):
        verbose_name = self._meta.get_field("timestamp").verbose_name
        self.assertEqual(verbose_name, "Время отправки")

    def test_timestamp_auto_now_add(self):
        auto_now_add = self._meta.get_field("timestamp").auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_status_label(self):
        verbose_name = self._meta.get_field("status").verbose_name
        self.assertEqual(verbose_name, "Статус отправки")

    def test_subscription_label(self):
        verbose_name = self._meta.get_field("subscription").verbose_name
        self.assertEqual(verbose_name, "Подписка")

    def test_subscription_null(self):
        obj = self._model.objects.all().first()
        obj.subscription = None
        with self.assertRaises(self.IntegrityError):
            obj.save()

    def test_subscription_related_name(self):
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            subscription_log_entry = subscription.mail_sending_journal.all()
            log_entries = self._model.objects.filter(subscription=subscription)
            self.assertEqual(subscription_log_entry.count(), log_entries.count())

    def test_model_ordering(self):
        log_entries = self._model.objects.all().order_by(", ".join(self._meta.ordering))
        self.assertLess(log_entries.first().timestamp, log_entries.last().timestamp)

    def test_model_verbose_name(self):
        self.assertEqual(self._meta.verbose_name, "Запись об отправке оповещения")

    def test_model_verbose_name_plural(self):
        self.assertEqual(self._meta.verbose_name_plural, "Журнал отправки оповещений")
