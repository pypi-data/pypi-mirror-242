import django_filters

from modules.ecology.models import Event, ParticipationUserEvent
from modules.ecology.models.participation_user_event import ParticipationStatus
from modules.integration.utils.filter import NumberInFilter


class EventFilter(django_filters.FilterSet):
    category = NumberInFilter()
    locality = NumberInFilter()

    maximum_offer_usage = django_filters.BooleanFilter(
        method="filter_by_maximum_offer_usage"
    )

    class Meta:
        model = Event
        fields = ['multiple_participation']

    @staticmethod
    def filter_by_maximum_offer_usage(queryset, _, value):
        # TODO Переделать фильтрацию, экстра фикс !!!!!
        res_pks = []
        for event in queryset:
            total_count = ParticipationUserEvent.objects.filter(
                event=event, status=ParticipationStatus.CONFIRMED).count()
            if (value and event.maximum_participants and total_count >= event.maximum_participants) or (
                    not value and (not event.maximum_participants or event.maximum_participants <= total_count)):
                res_pks.append(event.id)
        return queryset.filter(id__in=res_pks)
