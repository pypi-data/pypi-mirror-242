from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.viewsets.filters.voting import VotingFilter
from modules.core.models import User, Locality, Category
from modules.core.permissions import IsModerator
from modules.voting.api.serializers import (
    CategoryDetailsSerializer,
    LocalityDetailsSerializer, VoteModeratorListSerializer
)
from modules.voting.models import VoteState, Vote, VoteQuestion, VoteAnswerOption


class VotingModeratorAPI(viewsets.ReadOnlyModelViewSet):
    """API для голосований Модератора"""
    queryset = Vote.objects.none()
    permission_classes = [IsModerator]
    filterset_class = VotingFilter
    serializer_class = VoteModeratorListSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Vote.objects.all().distinct()\
            .order_by("-creation_date")\
            .prefetch_related(
                Prefetch("questions", queryset=VoteQuestion.objects.order_by("order")),
                Prefetch(
                    "questions__answers",
                    queryset=VoteAnswerOption.objects.order_by("order"),
                ),
            )

    def list(self, request: Request, *args, **kwargs):
        paginator = self.pagination_class()

        queryset = self.get_queryset()

        votes = self.filterset_class(
            data=request.query_params,
            queryset=queryset,
        ).qs

        page = paginator.paginate_queryset(queryset=votes, request=request)
        serializer = self.serializer_class(page, many=True)
        response = paginator.get_paginated_response(serializer.data)

        return response

    @action(methods=["get"], detail=False, url_path="info")
    def info(self, request: Request, *args, **kwargs):
        user: User = request.user
        vote_id = request.query_params.get("id")
        vote = Vote.objects.filter(pk=vote_id).first()
        if vote:
            if vote.author and vote.author.is_operator:
                localities = vote.author.sub_permissions.operator_permissions.voting_localities.all()
                categories = vote.author.sub_permissions.operator_permissions.voting_categories.all()
                data = {
                    "status": dict(VoteState.CHOICES),
                    "localities": LocalityDetailsSerializer(localities, many=True).data,
                    "categories": CategoryDetailsSerializer(categories, many=True).data
                }
            else:
                data = {
                    "status": dict(VoteState.CHOICES),
                    "localities": LocalityDetailsSerializer(vote.department.locality.all(), many=True).data,
                    "categories": CategoryDetailsSerializer(vote.department.sub_permissions.voting_categories.all(),
                                                            many=True).data
                }
        else:
            data = {
                "status": dict(VoteState.CHOICES),
                "localities": LocalityDetailsSerializer(Locality.objects.all(), many=True).data,
                "categories": CategoryDetailsSerializer(Category.objects.all(), many=True).data
            }
        return Response(data)
