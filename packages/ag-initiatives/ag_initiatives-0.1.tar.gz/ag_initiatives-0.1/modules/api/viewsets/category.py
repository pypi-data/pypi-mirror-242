from django_filters import rest_framework as filters
from rest_framework import viewsets

from modules.api.filters import CategoryFilter
from modules.api.serializers import CategoryShortSerializer
from modules.core.models import Category


class CategoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryShortSerializer
