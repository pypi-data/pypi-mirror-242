import uuid

from django import forms
from django.contrib import admin, messages
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as UserAdminContrib
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import caches
from django.db import models
from django.utils.translation import gettext as _

from modules.core.mixins import TrackUserMixin
from modules.core.models import User, UserRole, AdminLkoPermissions, OperatorLkoPermissions, SubPermissions, MailInvite
from modules.core.services import MailInviteService


def get_esia_raw_data(modeladmin, request, queryset):
    user = request.user
    if not user.is_active or not user.is_staff:
        messages.error(request, "Недостаточно прав")
        return

    if queryset.count() != 1:
        messages.error(request, "Необходимо выбрать одного пользователя")
        return

    selected_user = queryset[0]

    esia_data_cache = caches["esia_raw_data"]
    esia_data = esia_data_cache.get(selected_user.pk)

    messages.success(request, esia_data)


get_esia_raw_data.short_description = "Данные ЕСИА"


def remove_esia_raw_data(modeladmin, request, queryset):
    user = request.user
    selected_user = queryset[0]

    if not user.is_active or (not user.is_staff and not user.username == selected_user.username):
        messages.error(request, "Недостаточно прав")
        return

    if len(queryset) != 1:
        messages.error(request, "Необходимо выбрать одного пользователя")
        return

    selected_user.is_active = False
    selected_user.deletion_date = None
    selected_user.snils = None
    selected_user.username = uuid.uuid4()
    selected_user.roles = [UserRole.USER]
    selected_user.save()

    esia_data_cache = caches["esia_raw_data"]
    esia_data_cache.delete(selected_user.pk)

    messages.success(request, "Данные ЕСИА удалены")


remove_esia_raw_data.short_description = "Удалить данные ЕСИА"


class RolesFilter(admin.ChoicesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg = "%s__contains" % field_path
        self.lookup_val = params.get(self.lookup_kwarg)


class ArchiveFilter(admin.SimpleListFilter):
    title = "Архивированные учетные записи пользователей"
    parameter_name = "is_archive"

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_archive=True)
        elif self.value() == 'no':
            return queryset.filter(is_archive=False)


class AdminLkoPermissionsInline(admin.StackedInline):
    model = AdminLkoPermissions


class OperatorLkoPermissionsInline(admin.StackedInline):
    model = OperatorLkoPermissions
    exclude = (
        'voting_municipalities',
        'initiatives_municipalities',
        'map_works_municipalities',
        'plans_municipalities',
    )


class UsernameField(forms.CharField):
    def to_python(self, value):
        try:
            return super().to_python(value)
        except TypeError:
            return None


class MyUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        required=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}


@admin.register(User)
class UserAdmin(TrackUserMixin, UserAdminContrib):
    change_form_template = "core/admin/user_admin/change_form.html"
    add_form_template = "core/admin/user_admin/change_form.html"
    add_form = MyUserCreationForm
    inlines = [AdminLkoPermissionsInline, OperatorLkoPermissionsInline]
    list_display_links = ('first_name', 'last_name')

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        if hasattr(self, 'mail_send') and self.mail_send:
            self.mail_send = None
            return self.changelist_view(request, extra_context)
        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        obj = form.instance
        obj.refresh_from_db()
        if not hasattr(obj, 'sub_permissions'):
            sub_permissions = SubPermissions.objects.create(
                email=obj.work_email,
            )
        else:
            sub_permissions = obj.sub_permissions
        if hasattr(obj, 'admin_lko_permissions') and (admin_lko_permissions := obj.admin_lko_permissions):
            if hasattr(sub_permissions, 'admin_lko_permissions') and sub_permissions.admin_lko_permissions:
                ap = sub_permissions.admin_lko_permissions
                ap.sub_permissions = None
                ap.save()
            else:
                sub_permissions.admin_lko_permissions = obj.admin_lko_permissions
                sub_permissions.save()
        else:
            sub_permissions.admin_lko_permissions = None
            sub_permissions.save()
        if hasattr(obj, 'operator_permissions') and obj.operator_permissions:
            if hasattr(sub_permissions, 'operator_permissions') and (operator_permissions := obj.operator_permissions):
                op = sub_permissions.operator_permissions
                op.user_sub_permissions = None
                op.save()
            else:
                sub_permissions.operator_permissions = obj.operator_permissions
                sub_permissions.save()
        else:
            sub_permissions.operator_permissions = None
            sub_permissions.save()

        if (not change) and (UserRole.ADMIN_LKO in obj.roles or UserRole.OPERATOR in obj.roles):
            mail_invite = MailInvite.objects.create(
                first_name=obj.first_name,
                last_name=obj.last_name,
                patronymic_name=obj.patronymic_name,
                email=obj.work_email,
                phone=obj.phone,
                work_phone=obj.work_phone,
                sub_permission=sub_permissions,
                slug=MailInviteService().unique_slug_generator(),
                roles=obj.roles,
            )
            host = MailInviteService().get_host(request)
            MailInviteService().send_invite_message(mail_invite, host)
            self.message_user(
                request,
                f"Уведомление отправлено на почту",
                level=messages.SUCCESS,
            )
            self.mail_send = mail_invite
            if hasattr(sub_permissions, 'operator_permissions'):
                sub_permissions.operator_permissions.user = None
                sub_permissions.operator_permissions.save()
            if hasattr(sub_permissions, 'admin_lko_permissions'):
                sub_permissions.admin_lko_permissions.user = None
                sub_permissions.admin_lko_permissions.save()
            obj.delete()
            return
        obj.save()
        sub_permissions.user = obj
        sub_permissions.save()
        if hasattr(obj, 'admin_lko_permissions'):
            sub_permissions.admin_lko_permissions = obj.admin_lko_permissions
            obj.admin_lko_permissions.save()
        if hasattr(obj, 'operator_permissions'):
            sub_permissions.operator_permissions = obj.operator_permissions
            obj.operator_permissions.save()

    def get_translated_roles(self, obj: User) -> str:
        string_roles = ""
        for role in obj.roles:
            string_roles += f"{UserRole.RESOLVER.get(role)}, "

        if len(string_roles):
            string_roles = string_roles[:-2]

        return string_roles

    get_translated_roles.short_description = "Роли пользователей"

    def get_translated_categories(self, obj: User) -> str:
        string_categories = ""
        for category in obj.categories.all():
            string_categories += f"{category}, "

        if len(string_categories):
            string_categories = string_categories[:-2]

        return string_categories

    get_translated_categories.short_description = "Категории"

    list_display = ["last_name", "first_name", "patronymic_name", "get_translated_roles", "get_translated_categories"]

    search_fields = ["first_name", "last_name", "patronymic_name", "email", "phone", "department__name"]

    actions = [get_esia_raw_data, remove_esia_raw_data]

    readonly_fields = [
        "esia_id",
    ]

    list_filter = [
        "is_active",
        "is_staff",
        ArchiveFilter,
        "is_superuser",
        ("roles", RolesFilter),  # MultiSelectField,
        "department",
        "categories",
    ]

    fieldsets = (
        [None, {"fields": ["username", "password"]}],
        [
            _("Personal info"),
            {
                "fields": [
                    "snils",
                    "last_name",
                    "first_name",
                    "patronymic_name",
                    "birth_date",
                    "email",
                    "phone",
                    "work_phone",
                    "sub_phone",
                    "email_initiative_notification",
                    "work_email",
                    "position",
                    "department",
                    "roles",
                    "is_archive",
                    "categories",
                    "residential_locality",
                    "registration_locality",
                    "esia_id",
                    "esia_verified",
                ]
            },
        ],
        [
            _("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ],  # , 'user_permissions'
            },
        ],
        [_("Important dates"), {"fields": ("last_login", "date_joined")}],
    )

    add_fieldsets = [
        [None, {"fields": ["username", "password1", "password2"]}],
        [
            _("Personal info"),
            {
                "fields": [
                    "last_name",
                    "first_name",
                    "patronymic_name",
                    "email",
                    "phone",
                    "work_phone",
                    "sub_phone",
                    "email_initiative_notification",
                    "work_email",
                    "position",
                    "department",
                    "roles",
                    # "organization",
                    "is_archive",
                    "categories"
                ]
            },
        ],
        [
            _("Permissions"),
            {
                "fields": ["is_active", "is_staff", "is_superuser"],
            },
        ],
    ]
    filter_horizontal = ("categories",)

    formfield_overrides = {
        models.TextField: {"widget": forms.TextInput(attrs={"style": "width: 50em"})},
    }
