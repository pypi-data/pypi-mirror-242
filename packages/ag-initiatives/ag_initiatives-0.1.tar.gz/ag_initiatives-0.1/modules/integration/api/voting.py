from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters

from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.core.models import Locality, Category
from modules.integration.api.filters.voting import VoteFilter
from modules.integration.api.serializers.voting import VoteListSerializer
from modules.integration.permissions import CanGetVotes
from modules.voting.models import Vote, VoteQuestion, UserVote


class VoteAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VoteFilter
    serializer_class = VoteListSerializer
    permission_classes = [CanGetVotes]
    authentication_classes = [ExternalSystemTokenAuthentication]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Vote.objects.select_related(
            "department",
            "image",
            "brief_image",
            "video",
            "file",
        ).prefetch_related(
            "participants_groups",
            "participants_categories",
            Prefetch(
                "questions",
                queryset=VoteQuestion.objects.prefetch_related(
                    "answers",
                    "photo",
                    "video",
                    "file",
                    Prefetch(
                        "uservote_set",
                        queryset=UserVote.objects.all()
                    )
                ),
            ),
            Prefetch(
                "category",
                queryset=Category.objects.prefetch_related("images")
            ),
            Prefetch(
                "locality",
                queryset=Locality.objects.all().select_related("type"),
            )
        )
