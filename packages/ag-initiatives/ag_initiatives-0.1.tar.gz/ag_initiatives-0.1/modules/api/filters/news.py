import django_filters

from modules.core.models import News


class NewsFilter(django_filters.FilterSet):

    class Meta:
        model = News
        fields = [
            "is_public",
        ]
