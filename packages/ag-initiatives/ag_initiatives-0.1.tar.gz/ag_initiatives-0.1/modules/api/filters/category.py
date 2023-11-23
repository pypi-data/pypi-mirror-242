from django_filters import rest_framework as filters

from modules.core.models import Locality, Category


class CategoryFilter(filters.FilterSet):
    locality = filters.ModelChoiceFilter(
        field_name="locality", to_field_name="id", queryset=Locality.objects.all()
    )

    class Meta:
        model = Category
        fields = ("locality",)
