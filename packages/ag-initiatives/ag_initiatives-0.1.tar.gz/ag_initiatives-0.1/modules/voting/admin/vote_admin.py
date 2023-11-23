from django.utils.safestring import mark_safe
import nested_admin
from django.contrib import admin
from django import forms
from django.forms import TextInput

from modules.core.mixins import TrackUserMixin
from modules.core.models import Department
from modules.voting.mixins.vote_admin_mixin import VoteAdminMixin
from modules.voting.models import VoteQuestion, VoteAnswerOption, Vote


class VoteAdminForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = "__all__"
        exclude = ['participants_groups']
        widgets = {
            "topic": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteAnswerOptionAdminForm(forms.ModelForm):
    class Meta:
        model = VoteAnswerOption
        fields = "__all__"
        widgets = {"brief": TextInput(attrs={"size": 70})}


class VoteQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = VoteQuestion
        fields = "__all__"
        widgets = {
            "brief": TextInput(attrs={"size": 70}),
            "name": TextInput(attrs={"size": 70}),
        }


class VoteAnswerOptionAdmin(nested_admin.NestedStackedInline):
    form = VoteAnswerOptionAdminForm
    model = VoteAnswerOption
    extra = 0
    raw_id_fields = ["image"]


class VoteQuestionAdmin(nested_admin.NestedStackedInline):
    form = VoteQuestionAdminForm
    model = VoteQuestion
    extra = 0
    inlines = (VoteAnswerOptionAdmin,)
    raw_id_fields = ["photo", "video", "file"]


class StartDateTimeFilter(admin.filters.SimpleListFilter):
    title = 'Start DateTime'
    parameter_name = 'start_datetime'

    def lookups(self, request, model_admin):
        return (
            ('start_datetime', 'Start DateTime'),
        )

    def queryset(self, request, queryset):
        start_datetime = request.GET.get('start_datetime')
        if start_datetime:
            return queryset.filter(start_date__gte=start_datetime)
        return queryset

    template = 'voting/custom_start_datetime_filter.html'


class EndDateTimeFilter(admin.filters.SimpleListFilter):
    title = 'End DateTime'
    parameter_name = 'end_datetime'

    def lookups(self, request, model_admin):
        return (
            ('end_datetime', 'End DateTime'),
        )

    def queryset(self, request, queryset):
        end_datetime = request.GET.get('end_datetime')
        if end_datetime:
            return queryset.filter(end_date__lte=end_datetime)
        return queryset

    template = 'voting/custom_end_datetime_filter.html'


class CustomDepartmentFilter(admin.SimpleListFilter):
    title = 'Инициатор голосования'
    parameter_name = "department"

    def lookups(self, request, model_admin):
        departments = Department.objects.all()
        return [(department.id, department.name) for department in departments]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(department=value)
        return queryset


@admin.register(Vote)
class VoteAdmin(TrackUserMixin, VoteAdminMixin, nested_admin.NestedModelAdmin):
    form = VoteAdminForm
    list_display = [
        "name",
        "department_display",
        "category",
        "is_opened",
        "is_published",
        "start_date",
        "end_date",
        "voted_users_count",
        "state",
    ]
    list_filter = [
        StartDateTimeFilter,
        EndDateTimeFilter,
        "is_opened",
        "is_published",
        "category",
        CustomDepartmentFilter,
    ]
    inlines = (VoteQuestionAdmin,)
    raw_id_fields = ["author", "department", "brief_image", "image", "video", "file"]
    # actions = [vote_report, vote_report2]
    
    def department_display(self, obj: Vote):
        return mark_safe(f'<div style="width: 100px;">{obj.department.__str__() if obj.department else "Не указан"}</div>')
    department_display.short_description = 'Инициатор голосования'
    
    def voted_users_count(self, instance):
        return (
            instance.uservote_set.filter(locality__in=instance.locality.all())
            .distinct("user")
            .count()
        )
    
