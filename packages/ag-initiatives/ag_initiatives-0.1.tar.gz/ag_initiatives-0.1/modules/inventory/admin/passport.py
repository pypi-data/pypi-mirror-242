import nested_admin
from django import forms
from django.contrib import admin, messages
from django.db import models
from django.utils.translation import gettext as _
from django.forms import TextInput

from modules.core.models import User, UserRole
from modules.inventory.admin import inventory_admin_site
from modules.inventory.models import Passport, CommitteeParticipant, PassportFile


class PassportFileAdminForm(forms.ModelForm):
    class Meta:
        model = PassportFile
        fields = [
            "passport",
            "file",
        ]


class PassportFileAdminFormAdmin(nested_admin.NestedStackedInline):
    form = PassportFileAdminForm
    model = PassportFile
    extra = 0

    def has_add_permission(self, request):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False

    def has_change_permission(self, request, obj=None):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False


class CommitteeParticipantAdminForm(forms.ModelForm):
    class Meta:
        model = CommitteeParticipant
        fields = "__all__"
        widgets = {
            "organization": TextInput(attrs={"size": 70}),
            "position": TextInput(attrs={"size": 70}),
            "last_name": TextInput(attrs={"size": 70}),
            "first_name": TextInput(attrs={"size": 70}),
            "patronymic_name": TextInput(attrs={"size": 70}),
        }


class CommitteeParticipantAdminFormAdmin(nested_admin.NestedStackedInline):
    form = CommitteeParticipantAdminForm
    model = CommitteeParticipant
    extra = 0

    def has_add_permission(self, request):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False

    def has_change_permission(self, request, obj=None):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False


# class PassportAdminForm(forms.ModelForm):
#     class Meta:
#         model = Passport
#         fields = '__all__'
#
#     def clean(self, *args, **kwargs):
#         return super().clean()


# @admin.register(Passport, inventory_admin_site)
class PassportAdmin(nested_admin.NestedModelAdmin):
    list_display = [
        "department",
        "inventory_date",
        "name",
    ]

    fieldsets = (
        [
            _("Общие сведения"),
            {
                "fields": [
                    "locality_name",
                    "real_location",
                    "name",
                    "total_area",
                    "purpose",
                    "cadastral_number",
                    "livability_level",
                    "people_number_has_comfortable_access",
                    "extraneous_presence",
                ]
            },
        ],
        [
            _("Освещение"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("illumination_availability", "illumination_availability_note"),
                    (
                        "illumination_elements_number",
                        "illumination_elements_number_note",
                    ),
                    (
                        "illumination_technical_status",
                        "illumination_technical_status_note",
                    ),
                    ("illumination_sufficiently", "illumination_sufficiently_note"),
                ],
            },
        ],
        [
            _("Скамейки"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("benches_availability", "benches_availability_note"),
                    ("benches_number", "benches_number_note"),
                    ("benches_technical_status", "benches_technical_status_note"),
                    ("benches_sufficiently", "benches_sufficiently_note"),
                ],
            },
        ],
        [
            _("Урны для мусора"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("trash_cans_availability", "trash_cans_availability_note"),
                    ("trash_cans_number", "trash_cans_number_note"),
                    ("trash_cans_technical_status", "trash_cans_technical_status_note"),
                    ("trash_cans_sufficiently", "trash_cans_sufficiently_note"),
                ],
            },
        ],
        [
            _("Дорожное покрытие проезжей части"),
            {
                "classes": ["collapse"],
                "fields": [
                    (
                        "road_surface_technical_status",
                        "road_surface_technical_status_note",
                    ),
                ],
            },
        ],
        [
            _("Контейнерные площадки"),
            {
                "classes": ["collapse"],
                "fields": [
                    (
                        "container_platform_availability",
                        "container_platform_availability_note",
                    ),
                ],
            },
        ],
        [
            _("Пешеходные дорожки"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("walking_path_availability", "walking_path_availability_note"),
                    ("walking_path_repairs_needed", "walking_path_repairs_needed_note"),
                ],
            },
        ],
        [
            _("Детские площадки, игровое оборудование"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("playground_availability", "playground_availability_note"),
                    ("playground_name", "playground_name_note"),
                    ("playground_number", "playground_number_note"),
                    ("playground_technical_status", "playground_technical_status_note"),
                    ("playground_sufficiently", "playground_sufficiently_note"),
                ],
            },
        ],
        [
            _("Спортивные площадки, спортивное оборудование"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("sportsground_availability", "sportsground_availability_note"),
                    ("sportsground_name", "sportsground_name_note"),
                    ("sportsground_number", "sportsground_number_note"),
                    (
                        "sportsground_technical_status",
                        "sportsground_technical_status_note",
                    ),
                    ("sportsground_sufficiently", "sportsground_sufficiently_note"),
                ],
            },
        ],
        [
            _("Площадки для отдыха"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("vacation_spot_availability", "vacation_spot_availability_note"),
                    ("vacation_spot_name", "vacation_spot_name_note"),
                    ("vacation_spot_number", "vacation_spot_number_note"),
                    (
                        "vacation_spot_technical_status",
                        "vacation_spot_technical_status_note",
                    ),
                    ("vacation_spot_sufficiently", "vacation_spot_sufficiently_note"),
                ],
            },
        ],
        [
            _("Зеленые зоны"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("green_area_availability", "green_area_availability_note"),
                    ("green_area_name", "green_area_name_note"),
                    ("green_area_number", "green_area_number_note"),
                    ("green_area_technical_status", "green_area_technical_status_note"),
                    ("green_area_sufficiently", "green_area_sufficiently_note"),
                ],
            },
        ],
        [
            _(
                "Наличие приспособлений для маломобильных групп населения (опорных поручней, специального оборудования на детских и спортивных площадках; спусков, пандусов для обеспечения беспрепятственного перемещения)"
            ),
            {
                "classes": ["collapse"],
                "fields": [
                    (
                        "lowmobility_groups_facilities_availability",
                        "lowmobility_groups_facilities_availability_note",
                    ),
                ],
            },
        ],
        [
            _("Иное"),
            {
                "classes": ["collapse"],
                "fields": [
                    ("others", "others_note"),
                ],
            },
        ],
        [
            None,
            {
                "fields": [
                    "inventory_date",
                ]
            },
        ],
    )

    formfield_overrides = {
        models.TextField: {
            "widget": forms.TextInput(
                # attrs={"style": "width: 50em"}
            )
        },
    }

    # form = PassportAdminForm

    inlines = [
        PassportFileAdminFormAdmin,
        CommitteeParticipantAdminFormAdmin,
    ]

    def get_queryset(self, request):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            super().get_queryset(request).filter(department=request.user.department)

        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        user: User = request.user

        obj.department = user.department

        # if user_department is None:
        #     messages.error(request, 'У пользователя не установлено ведомство')
        #     return False
        #     # raise forms.ValidationError("У пользователя не установлено ведомство")
        #
        # if user_department.inventory_locality is None:
        #     messages.error(request, 'У ведомства пользователя не установлено МО')
        #     return False
        #     # raise forms.ValidationError("У ведомства пользователя не установлено МО")

        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False

    def has_delete_permission(self, request, obj=None):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False

    def has_change_permission(self, request, obj=None):
        user: User = request.user

        if UserRole.INVENTORY_LOCAL_GOVERNMENT in user.roles:
            return True

        return False
