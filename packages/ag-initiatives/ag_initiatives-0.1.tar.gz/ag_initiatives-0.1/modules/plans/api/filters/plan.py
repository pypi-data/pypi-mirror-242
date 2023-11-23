import django_filters

from modules.plans.models import Category, Plan


class PlanFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    department = django_filters.NumberFilter(method="filter_department")

    class Meta:
        model = Plan
        fields = [
            "category",
            "locality",
            "department"
        ]

    def filter_department(self, queryset, name, value: int):
        return queryset.filter(owner__id=value)
