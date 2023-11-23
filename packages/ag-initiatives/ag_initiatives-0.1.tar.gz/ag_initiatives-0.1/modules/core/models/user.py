import collections

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, Case, When, OuterRef, Subquery, Count, ExpressionWrapper, Sum, Value
from django.utils import timezone
from django.utils.translation import gettext as _
from multiselectfield import MultiSelectField

from modules.core.models import DepartmentStatus
from modules.initiatives.models import (
    Initiative,
    InitiativeState,
    InitiativeOperatorCommunication,
)
from modules.initiatives.models.initiative_operator_communication import (
    ModerateResponseState,
)
from modules.initiatives.utils.annotator import Annotator


class UserRole(object):
    ADMIN = "ADMIN_MAIN"
    ADMIN_LKO = "ADMIN_LKO"
    OPERATOR = "OPERATOR_MAIN"
    MODERATOR = "MODERATOR"
    SUPPORT = "SUPPORT"
    USER = "USER"
    # OPERATOR_OPINION = "OPERATOR_OPINION"
    # OPERATOR_LKO = "OPERATOR_LKO"
    # ORGANIZER = "ORGANIZER"
    # PARTNER = "PARTNER"
    # SECRETARY = "SECRETARY"
    # CURATOR = "CURATOR"
    # INVENTORY_LOCAL_GOVERNMENT = "INVENTORY_LOCAL_GOVERNMENT"
    # INVENTORY_EXECUTIVE_AUTHORITY = "INVENTORY_EXECUTIVE_AUTHORITY"

    RESOLVER = collections.OrderedDict(
        [
            (ADMIN, "Администратор"),
            (ADMIN_LKO, "Администратор ЛКО"),
            (OPERATOR, "Оператор"),
            (MODERATOR, "Модератор"),
            (SUPPORT, "Техподдержка"),
            (USER, "Пользователь"),
            # (OPERATOR_OPINION, "Обратная связь. Оператор"),
            # (ORGANIZER, "Организатор"),
            # (PARTNER, "Партнер"),
            # (SECRETARY, "Пресс-секретарь"),
            # (CURATOR, "Куратор"),
            # (
            #     INVENTORY_LOCAL_GOVERNMENT,
            #     "Инвентаризация. Орган местного самоуправления",
            # ),
            # (
            #     INVENTORY_EXECUTIVE_AUTHORITY,
            #     "Инвентаризация. Орган исполнительной власти",
            # ),
        ]
    )

    CHOICES = RESOLVER.items()


class User(AbstractUser):
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.",
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Пользователь с таким именем пользователя уже существует.",
        },
        blank=True, null=True,
    )
    password = models.CharField(
        "Пароль",
        max_length=128,
        blank=True, null=True,
    )
    first_name = models.TextField(
        verbose_name=_("Имя"),
        null=False,
        blank=False,
    )
    last_name = models.TextField(
        verbose_name=_("Фамилия"),
        null=True,
        blank=True,
    )
    patronymic_name = models.TextField(
        verbose_name=_("Отчество"),
        null=True,
        blank=True,
    )
    gender = models.TextField(
        verbose_name=_("Пол"),
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name=_("Дата рождения"),
        null=True,
        blank=True,
    )
    phone = models.TextField(
        verbose_name=_("Номер телефона"),
        blank="True",
    )
    work_phone = models.CharField(
        max_length=12,
        verbose_name="Рабочий номер телефона",
        blank=True,
        null=True,
    )
    sub_phone = models.CharField(
        max_length=12,
        verbose_name="Добавочный номер телефона",
        null=True,
        blank=True
    )
    position = models.CharField(
        max_length=255,
        verbose_name="Должность",
        null=True,
        blank=True,
    )
    department = models.ForeignKey(
        to="core.Department",
        verbose_name="Организации, к которым пользователь имеет доступ",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )
    # todo переименовать в email_notification
    email_initiative_notification = models.BooleanField(
        verbose_name="Уведомления по почте",
        default=True,
    )
    email_appeals_notification = models.BooleanField(
        verbose_name="Уведомления по почте для ПОС",
        default=True,
    )
    work_email = models.EmailField(
        verbose_name="Рабочая электронная почта",
        blank=True,
    )

    residential_locality = models.ForeignKey(
        to="core.Locality",
        related_name="user_residential",
        verbose_name="МО проживания",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    registration_locality = models.ForeignKey(
        to="core.Locality",
        related_name="user_registration",
        verbose_name="МО регистрации",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    esia_verified = models.BooleanField(
        verbose_name="Подтвержденный ЕСИА аккаунт",
        default=False,
    )

    roles = MultiSelectField(
        choices=UserRole.CHOICES,
        verbose_name="Роли пользователей",
    )
    categories = models.ManyToManyField(
        to="core.CategoryCitizen",
        blank=True,
        verbose_name="Категории гражданина",
        related_name="users"
    )
    is_archive = models.BooleanField(
        verbose_name="В архиве",
        default=False,
        blank=False,
        null=False,
    )
    deletion_date = models.DateTimeField(
        verbose_name="Дата удаления учётной записи",
        blank=True,
        null=True,
    )
    snils = models.CharField(
        "СНИЛС",
        max_length=20,
        unique=True,
        blank=True, null=True,
    )

    # def clean(self):
    #     """
    #     Если пользователь в архиве (is_archive=True) --> редактирование ролей невозможно.
    #     """
    #     if self.is_archive and self.pk:
    #         original_user = User.objects.get(pk=self.pk)
    #         if original_user.is_archive and self.roles != original_user.roles:
    #             raise ValidationError("Пользователь в архиве. Изменение ролей невозможно.")

    @property
    def esia_id(self):
        return self.username

    def get_locality_for_initiative(self):
        if self.residential_locality is not None:
            return self.residential_locality

        if self.registration_locality is not None:
            return self.registration_locality

        return None

    @property
    def age(self):
        return (
            int((timezone.now().date() - self.birth_date).days / 365.25)
            if self.birth_date
            else None
        )

    @property
    def is_admin(self):
        return UserRole.ADMIN in self.roles

    @property
    def is_admin_lko(self):
        return UserRole.ADMIN_LKO in self.roles and not self.is_archive and hasattr(self, "sub_permissions")

    @property
    def is_moderator(self):
        return UserRole.MODERATOR in self.roles and not self.is_archive

    @property
    def is_operator(self):
        return UserRole.OPERATOR in self.roles and not self.is_archive and hasattr(self, "sub_permissions")

    # @property
    # def is_operator_opinion(self):
    #     return UserRole.OPERATOR_OPINION in self.roles

    @property
    def is_simple_user(self):
        return UserRole.USER in self.roles

    @property
    def initiatives_for_actions(self):
        if self.is_operator and self.department:
            return self._operator_initiatives_for_actions_base_query
        elif self.is_moderator:
            return self._moderator_initiatives_for_actions
        elif self.is_simple_user:
            return self.user_initiatives_for_actions
        return Initiative.objects.none()

    @property
    def operator_initiatives_for_actions(self):
        return self._operator_initiatives_for_actions_base_query

    @property
    def operator_initiatives_for_view_access(self):
        if self.is_operator:
            department = self.sub_permissions.operator_permissions.department
        else:
            department = self.department

        if department.additional_filtering:
            return self._operator_initiatives_for_actions_base_query.union(
                self._operator_additional_initiatives_base_query
            )
        return self._operator_initiatives_for_actions_base_query

    @property
    def moderator_initiatives_for_actions(self):
        return self._moderator_initiatives_for_actions

    @property
    def initiatives_for_view(self):
        if self.is_operator and self.department:
            return self.operator_all_initiatives_for_view.order_by(
                "sort_field", "-creation_date_time"
            )
        elif self.is_moderator:
            return self.moderator_initiatives_for_view.order_by("-creation_date_time")
        elif self.is_simple_user:
            return self.user_initiatives_for_view.order_by("-creation_date_time")
        return Initiative.objects.none()

    @property
    def initiatives_for_count(self):
        # if self.is_operator and self.department:
        #     return self._operator_all_initiatives_count
        # elif self.is_moderator:
        #     return self._moderator_initiatives_count
        # elif self.is_simple_user:
        return self._user_initiatives_count
        # return 0

    @property
    def _operator_all_initiatives_count(self):
        if self.is_operator:
            department = self.sub_permissions.operator_permissions.department
        else:
            department = self.department

        if department.additional_filtering:
            return self._operator_initiatives_for_actions_base_query.union(
                self._operator_additional_initiatives_base_query
            ).count()
        return self._operator_initiatives_for_actions_base_query.count()

    @property
    def _operator_initiatives_for_actions_base_query(self):
        if self.is_operator:
            department = self.sub_permissions.operator_permissions.department
        else:
            department = self.department

        return Initiative.objects.filter(
            settings__department=department,
            state__in=[
                InitiativeState.REJECTED,
                InitiativeState.REJECTED_VOTES_THRESHOLD,
                InitiativeState.MODERATION,
                InitiativeState.VOTES_COLLECTION,
                InitiativeState.CONSIDERATION,
                InitiativeState.ACCOMPLISHED,
                InitiativeState.IN_PROGRESS,
            ],
        )

    @property
    def _operator_base_initiatives_for_view(self):
        return self._operator_initiatives_for_actions_base_query.select_related(
            "category", "category__parent"
        ).prefetch_related('locality')

    @property
    def operator_lko_all_initiatives_for_view(self):
        department = self.sub_permissions.operator_permissions.department

        if department.additional_filtering:
            return Annotator.union(
                self._operator_base_initiatives_for_view,
                self._operator_additional_initiatives_for_view,
            )
        return Annotator.annotate_for_sorting(self._operator_base_initiatives_for_view)

    @property
    def operator_all_initiatives_for_view(self):
        if self.is_operator:
            department = self.sub_permissions.operator_permissions.department
        else:
            department = self.department

        operator_base_initiatives_for_view = Initiative.objects.filter(
            settings__department=self.department,
            state__in=[
                InitiativeState.REJECTED,
                InitiativeState.REJECTED_VOTES_THRESHOLD,
                InitiativeState.MODERATION,
                InitiativeState.VOTES_COLLECTION,
                InitiativeState.CONSIDERATION,
                InitiativeState.ACCOMPLISHED,
                InitiativeState.IN_PROGRESS,
            ], ) \
            .select_related("category", "category__parent") \
            .prefetch_related('locality')

        operator_additional_initiatives_for_view = Initiative.objects.filter(
            ~Q(settings__department=self.department),
            Q(locality__in=department.locality.all())
            & Q(category__in=department.sub_permissions.initiative_categories.all())
            & Q(
                state__in=[
                    InitiativeState.MODERATION,
                    InitiativeState.REJECTED,
                    InitiativeState.VOTES_COLLECTION,
                    InitiativeState.REJECTED_VOTES_THRESHOLD,
                    InitiativeState.CONSIDERATION,
                    InitiativeState.ACCOMPLISHED,
                    InitiativeState.IN_PROGRESS,
                ]
            ),
        ) \
            .select_related("category", "category__parent") \
            .prefetch_related('locality')

        if department.additional_filtering:
            return Annotator.union(
                operator_base_initiatives_for_view,
                operator_additional_initiatives_for_view,
            )
        return Annotator.annotate_for_sorting(operator_base_initiatives_for_view)

    @property
    def _operator_additional_initiatives_base_query(self):
        if self.is_operator:
            department = self.sub_permissions.operator_permissions.department
        else:
            department = self.department

        return Initiative.objects.filter(
            ~Q(settings__department=department),
            Q(locality__in=department.locality.all())
            & Q(category__in=department.sub_permissions.initiative_categories.all())
            & Q(
                state__in=[
                    InitiativeState.MODERATION,
                    InitiativeState.REJECTED,
                    InitiativeState.VOTES_COLLECTION,
                    InitiativeState.REJECTED_VOTES_THRESHOLD,
                    InitiativeState.CONSIDERATION,
                    InitiativeState.ACCOMPLISHED,
                    InitiativeState.IN_PROGRESS,
                ]
            ),
        )

    @property
    def _operator_additional_initiatives_for_view(self):
        return self._operator_additional_initiatives_base_query.select_related(
            "category", "category__parent"
        ).prefetch_related('locality')

    @property
    def _moderator_initiatives_for_actions(self):
        subquery = (
            InitiativeOperatorCommunication.objects.filter(
                Q(initiative=OuterRef("pk"))
                & Q(state=ModerateResponseState.MODERATION_REQUIRED)
            )
                .values("initiative")
                .annotate(count=Count("initiative"))
                .values("count")
        )
        return (
            Initiative.objects.filter(
                state__in=(
                    InitiativeState.PREMODERATION,
                    InitiativeState.CHANGES_APPROVAL,
                    InitiativeState.MODERATION,
                )
            )
                .annotate(
                messages_count=Case(
                    When(
                        Q(state=InitiativeState.MODERATION),
                        then=ExpressionWrapper(
                            Subquery(subquery), output_field=models.IntegerField()
                        ),
                    ),
                    default=None,
                )
            )
                .filter(Q(messages_count__gt=0) | ~Q(state=InitiativeState.MODERATION))
        )

    @property
    def _moderator_initiatives_count(self):
        return self._moderator_initiatives_for_actions.count()

    @property
    def moderator_initiatives_for_view(self):
        subquery = InitiativeOperatorCommunication.objects.filter(
            state=ModerateResponseState.MODERATION_REQUIRED
        ).values("initiative").annotate(count=Count("initiative")).values("count")[:1]

        return (
            self._moderator_initiatives_for_actions.select_related(
                "category", "category__parent"
            ).prefetch_related(
                'locality'
            ).annotate(
                messages_count=Case(
                    When(
                        Q(state=InitiativeState.MODERATION),
                        then=ExpressionWrapper(
                            Subquery(subquery), output_field=models.IntegerField()
                        ),
                    ),
                    default=None,
                )
            )
                .filter(Q(messages_count__gt=0) | ~Q(state=InitiativeState.MODERATION))
        )

    @property
    def _user_initiatives_count(self):
        return self.user_initiatives_for_actions.count()

    @property
    def user_initiatives_for_actions(self):
        return self.initiative_set.all()

    @property
    def user_initiatives_for_view(self):
        return self.user_initiatives_for_actions.select_related(
            "category", "category__parent"
        ).prefetch_related('locality')

    @property
    def ecology(self):
        from modules.ecology.models import UserProfile as EcologyUserProfile

        instance, created = EcologyUserProfile.objects.get_or_create(user=self)
        return instance

    class Meta:
        verbose_name = "Пользователь системы"
        verbose_name_plural = "Пользователи системы"

    def __str__(self):
        return "{} {} {}".format(self.first_name, self.patronymic_name, self.last_name)
