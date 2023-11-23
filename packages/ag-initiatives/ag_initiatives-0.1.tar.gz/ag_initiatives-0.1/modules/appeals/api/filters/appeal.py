import django_filters

from modules.appeals.models import Category, Appeal, AppealState


class AppealFilter(django_filters.FilterSet):
    category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all())
    state = django_filters.MultipleChoiceFilter(
        choices=[(k, v) for k, v in AppealState.CHOICES]
    )

    class Meta:
        model = Appeal
        fields = [
            "category",
            "locality",
            "state",
        ]
