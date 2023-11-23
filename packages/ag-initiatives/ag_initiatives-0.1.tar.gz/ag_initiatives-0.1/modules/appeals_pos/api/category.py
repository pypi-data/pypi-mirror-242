from django.db.models import Prefetch
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.response import Response

from modules.appeals_pos.models.category import Category
from modules.appeals_pos.models.subcategory import Subcategory
from modules.appeals_pos.serializers import CategoryTreeSerializer


class CategoryApi(viewsets.ViewSet):

    serializer_class = CategoryTreeSerializer
    queryset = Category.objects.filter(deleted=False).order_by('name').prefetch_related(
        Prefetch('subcategories', queryset=Subcategory.objects.order_by('name'))
    )

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class

    @never_cache
    def list(self, request):
        serializer = self.get_serializer_class()(self.queryset, many=True)
        return Response(serializer.data)
