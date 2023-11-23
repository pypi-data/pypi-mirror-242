import collections

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition

from modules.initiatives.enums import InitiativeTypes
from modules.initiatives.mixins.initiative_get_queryset_override import InitiativeGetQuerysetOverride
from modules.initiatives.models import InitiativeOperatorCommunicationType
from modules.initiatives.models.initiative_operator_communication import (
    PremoderateChangesResponseDecision,
)
from modules.initiatives.service.email_builder import EmailBuilder, EmailSender
from modules.initiatives.service.state_changer import InitiativeStateChanger
from modules.initiatives.tasks import end_votes_collection
from modules.initiatives.utils.mail_strings import EmailString
from modules.initiatives.utils.notify_text import NotifyText
from modules.core.models import user as CoreUserPackage
from modules.subscriptions.mixins.subscribe_mixin import SubscribeMixin


class InitiativeState(object):
    PREMODERATION = "PREMODERATION"  # Модерирование модератором
    PREMODERATION_REJECTED = "PREMODERATION_REJECTED"  # Модерирование модератором
    CHANGES_APPROVAL = "CHANGES_APPROVAL"
    MODERATION = "MODERATION"  # Модерирование оператором
    REJECTED = "REJECTED"
    CREATED = "CREATED"
    VOTES_COLLECTION = "VOTES_COLLECTION"
    REJECTED_VOTES_THRESHOLD = "REJECTED_VOTES_THRESHOLD"
    CONSIDERATION = "CONSIDERATION"
    IN_PROGRESS = "IN_PROGRESS"
    ACCOMPLISHED = "ACCOMPLISHED"

    RESOLVER = collections.OrderedDict(
        [
            (PREMODERATION, "Модерирование"),
            (PREMODERATION_REJECTED, "Отклонена по итогам модерации"),
            (CHANGES_APPROVAL, "Согласование изменений"),
            (MODERATION, "Экспертная оценка"),
            (REJECTED, "Отклонена"),
            (VOTES_COLLECTION, "Сбор голосов"),
            (REJECTED_VOTES_THRESHOLD, "Порог голосования не пройден"),
            (CONSIDERATION, "На рассмотрении"),
            (IN_PROGRESS, "Принято решение"),
            (ACCOMPLISHED, "Реализовано"),
        ]
    )

    CHOICES = RESOLVER.items()


PUBLISHED_STATES = [
    InitiativeState.VOTES_COLLECTION,
    InitiativeState.REJECTED_VOTES_THRESHOLD,
    InitiativeState.CONSIDERATION,
    InitiativeState.IN_PROGRESS,
    InitiativeState.ACCOMPLISHED,
]


class Initiative(InitiativeGetQuerysetOverride,
                 SubscribeMixin,
                 models.Model):
    number = models.TextField(
        verbose_name="Регистрационный номер",
    )
    creation_date_time = models.DateTimeField(
        verbose_name="Дата создания",
    )
    user = models.ForeignKey(
        to="core.User",
        verbose_name="Заявитель",
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        max_length=20,
        choices=InitiativeTypes.CHOICES,
        verbose_name='Уровень реализации',
    )
    email = models.TextField(
        verbose_name="Электронная почта",
    )
    category = models.ForeignKey(
        to="initiatives.InitiativeCategory",
        verbose_name="Категория",
        on_delete=models.CASCADE,
    )
    settings = models.ForeignKey(
        to="initiatives.InitiativeAcceptingSettings",
        on_delete=models.CASCADE,
    )
    locality = models.ManyToManyField(
        to="core.Locality",
        blank=True,
        verbose_name="Муниципальные образования",
        related_name='initiatives',
    )
    duration_month = models.PositiveIntegerField(
        verbose_name="Продолжительность голосования",
    )
    votes_threshold = models.PositiveIntegerField(
        verbose_name="Требуемое количество голосов",
    )
    title = models.TextField(
        verbose_name="Заголовок",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    expectations = models.TextField(
        verbose_name="Ожидаемый результат",
    )
    files = models.ManyToManyField(
        to="initiatives.InitiativeFile",
        verbose_name="Файлы",
    )
    state = FSMField(
        choices=InitiativeState.CHOICES,
        verbose_name="Статус",
    )
    moderation_begin_date = models.DateTimeField(
        verbose_name="Дата начала модерации",
        null=True,
        blank=True,
    )
    votes_collection_begin_date = models.DateTimeField(
        verbose_name="Дата начала сбора голосов",
        null=True,
        blank=True,
    )
    date_of_report_publication = models.DateTimeField(
        verbose_name="Дата публикации отчёта",
        null=True,
        blank=True,
    )
    date_of_decision = models.DateTimeField(
        verbose_name="Дата принятия решения",
        null=True,
        blank=True,
    )
    pdf_export = models.FileField(
        verbose_name="Данные об инициативе в .pdf", null=True, blank=True
    )

    def __str__(self):
        return self.number

    @transition(
        field="state",
        source=(InitiativeState.PREMODERATION,),
        target=InitiativeState.PREMODERATION_REJECTED,
    )
    def moderator_reject(self, user, validated_data):
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(
            new_state=InitiativeState.PREMODERATION_REJECTED
        )
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.PREMODERATE_REJECT,
            **validated_data
        )
        email_builder = EmailBuilder(self, EmailString.PREMODERATION_REJECTED)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @transition(
        field="state",
        source=(InitiativeState.PREMODERATION,),
        target=InitiativeState.MODERATION,
    )
    def moderator_accept(self, user):
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(new_state=InitiativeState.MODERATION)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.PREMODERATE_APPROVE,
            text=NotifyText.PREMODERATION_APPROVED,
        )
        email_builder = EmailBuilder(
            self,
            user_template_string=EmailString.PREMODERATION_ACCEPTED,
            operator_template_string=EmailString.PREMODERATION_ACCEPTED_OPERATOR,
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()
        email_sender.send_to_department_if_notifications_enabled()
        email_sender.send_operator_broadcast_with_department(initiative=self)

    @transition(
        field="state",
        source=(InitiativeState.PREMODERATION,),
        target=InitiativeState.CHANGES_APPROVAL,
    )
    def moderator_offer_changes(self, user, validated_data):
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_REQUEST,
            text=NotifyText.MODERATOR_OFFER_CHANGES,
            **validated_data
        )
        email_builder = EmailBuilder(self, EmailString.MODERATOR_OFFERED_CHANGES)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @transition(
        field="state",
        source=(InitiativeState.CHANGES_APPROVAL,),
        target=InitiativeState.PREMODERATION_REJECTED,
    )
    def user_reject_changes(self, user):
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(
            new_state=InitiativeState.PREMODERATION_REJECTED
        )
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_RESPONSE,
            decision=PremoderateChangesResponseDecision.REJECT,
            text=NotifyText.USER_REJECT_CHANGES,
        )
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.SYSTEM_NOTIFICATION,
            text=NotifyText.PREMODERATION_REJECTED,
            is_system_notification=True,
        )
        changer.mark_offered_changes_as_viewed(
            type=InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_REQUEST
        )
        email_builder = EmailBuilder(self, EmailString.PREMODERATION_REJECTED)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @transition(
        field="state",
        source=(InitiativeState.CHANGES_APPROVAL,),
        target=InitiativeState.MODERATION,
    )
    def user_accept_changes(self, user):
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(new_state=InitiativeState.MODERATION)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_RESPONSE,
            text=NotifyText.USER_ACCEPT_CHANGES,
        )
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.SYSTEM_NOTIFICATION,
            decision=PremoderateChangesResponseDecision.APPROVE,
            text=NotifyText.PREMODERATION_APPROVED,
            is_system_notification=True,
        )
        changer.mark_offered_changes_as_viewed(
            type=InitiativeOperatorCommunicationType.PREMODERATE_CHANGES_REQUEST
        )

        email_builder = EmailBuilder(
            self,
            EmailString.PREMODERATION_ACCEPTED,
            EmailString.PREMODERATION_ACCEPTED_OPERATOR,
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()
        email_sender.send_to_department_if_notifications_enabled()
        email_sender.send_operator_broadcast_with_department(initiative=self)

    @transition(
        field="state",
        source=(InitiativeState.MODERATION,),
        target=InitiativeState.REJECTED,
    )
    def operator_reject(self, user, validated_data):
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(new_state=InitiativeState.REJECTED)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.MODERATE_REJECT, **validated_data
        )
        email_builder = EmailBuilder(
            self,
            user_template_string=EmailString.MODERATION_REJECTED,
            role_broadcast_template_string=EmailString.MODERATION_REJECTED_TO_MODERATOR,
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()
        email_sender.send_role_broadcast(CoreUserPackage.UserRole.MODERATOR)

    @transition(
        field="state",
        source=(InitiativeState.MODERATION,),
        target=InitiativeState.VOTES_COLLECTION,
    )
    def operator_accept(self, user):
        self.votes_collection_begin_date = timezone.now()
        self.save()
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(
            new_state=InitiativeState.VOTES_COLLECTION
        )
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.MODERATE_APPROVE,
            text=NotifyText.MODERATION_APPROVED,
        )
        email_builder = EmailBuilder(
            self,
            user_template_string=EmailString.MODERATION_APPROVED,
            role_broadcast_template_string=EmailString.MODERATION_APPROVED_TO_MODERATOR,
        )
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()
        email_sender.send_role_broadcast(role=CoreUserPackage.UserRole.MODERATOR)
        end_votes_collection.apply_async(
            kwargs={"pk": self.pk}, eta=self.vote_finish_date
        )

    @transition(
        field="state",
        source=(InitiativeState.VOTES_COLLECTION,),
        target=InitiativeState.REJECTED_VOTES_THRESHOLD,
    )
    def time_exceeded(self):
        changer = InitiativeStateChanger(self)
        changer.create_initiative_state_change(
            new_state=InitiativeState.REJECTED_VOTES_THRESHOLD
        )
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.SYSTEM_NOTIFICATION,
            text=NotifyText.TIME_EXCEEDED,
            is_system_notification=True,
        )
        email_builder = EmailBuilder(self, EmailString.TIME_EXCEEDED)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @transition(
        field="state",
        source=(InitiativeState.VOTES_COLLECTION,),
        target=InitiativeState.CONSIDERATION,
    )
    def necessary_votes_collected(self):
        changer = InitiativeStateChanger(self)
        changer.create_initiative_state_change(new_state=InitiativeState.CONSIDERATION)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.SYSTEM_NOTIFICATION,
            text=NotifyText.NECESSARY_VOTES_COLLECTED,
            is_system_notification=True,
        )
        email_builder = EmailBuilder(self, EmailString.NECESSARY_VOTES_COLLECTED)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @transition(
        field="state",
        source=(InitiativeState.CONSIDERATION,),
        target=InitiativeState.IN_PROGRESS,
    )
    def publish_decision(self, user, validated_data):
        self.date_of_decision = timezone.now()
        self.save()
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(new_state=InitiativeState.IN_PROGRESS)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.IN_PROGRESS_NOTIFICATION,
            **validated_data
        )
        email_builder = EmailBuilder(self, EmailString.DECISION_PUBLISHED)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @transition(
        field="state",
        source=(InitiativeState.IN_PROGRESS,),
        target=InitiativeState.ACCOMPLISHED,
    )
    def accomplished(self, user, validated_data):
        self.date_of_report_publication = timezone.now()
        self.save()
        changer = InitiativeStateChanger(self, user)
        changer.create_initiative_state_change(new_state=InitiativeState.ACCOMPLISHED)
        changer.create_initiative_communication(
            type=InitiativeOperatorCommunicationType.ACCOMPLISHED_NOTIFICATION,
            **validated_data
        )
        email_builder = EmailBuilder(self, EmailString.ACCOMPLISHED)
        email_sender = EmailSender(email_builder)
        email_sender.send_to_user_if_notifications_enabled()

    @property
    def vote_finish_date(self):
        duration = (
            relativedelta(months=self.duration_month)
            if not settings.DEBUG_TIMER
            else relativedelta(seconds=self.duration_month)
        )
        return (
            self.votes_collection_begin_date + duration
            if self.votes_collection_begin_date
            else None
        )

    @property
    def type_name(self):
        return InitiativeTypes.RESOLVER[self.type]

    @property
    def state_name(self):
        return InitiativeState.RESOLVER[self.state]

    @property
    def votes_count(self):
        return self.user_initiative_approve.count()

    @property
    def is_published(self):
        return self.state in PUBLISHED_STATES

    @property
    def communications(self):
        return self.initiative_operator_communication.all()

    def is_owner(self, user):
        return self.user.pk == user.pk

    def is_voted(self, user):
        return self.user_initiative_approve.filter(user__pk=user.pk).count() > 0

    class Meta:
        verbose_name = "Инициатива"
        verbose_name_plural = "Инициативы"
