import collections
import logging
from typing import Union, List, Optional, Dict

from django.db import transaction
from django.db.models import Prefetch, Q
from django_filters import rest_framework as filters
from pydantic import BaseModel, validator
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from django.http.request import HttpRequest

from modules.api.filters import VoteLocalFilter, VoteLocalStatsFilter
from modules.api.serializers import (
    VoteLocalSerializer,
    VoteLocalDetailsSerializer,
    LocalitySerializer,
)
from modules.core.mixins.user_track_admin import TrackUserApiMixin
from modules.core.models import Locality, User
from modules.ecology.models import UserState
from modules.voting.api import LocalVotingGroupAPI
from modules.voting.api.serializers import LocalVotingGroupSerializer
# from modules.voting.enums import VoteType
from modules.voting.models import (
    VoteState,
    UserMunicipalVote,
    VoteLocal,
    VoteLocalQuestion,
    VoteLocalAnswer,
    LocalVotingGroup,
)

from modules.ecology.services.user_service import UserService as EcologyUserService
from modules.voting.services import URLGenerator
from .vote import AnswerDTO, AnswerType


class VoteLocalAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        VoteLocal.objects.filter(is_published=True)
        .prefetch_related(
            Prefetch("local_questions", queryset=VoteLocalQuestion.objects.order_by("order")),
            Prefetch(
                "local_questions__local_answers",
                queryset=VoteLocalAnswer.objects.order_by("order"),
            ),
        )
        .order_by("-start_date")
    )
    serializer_class = VoteLocalSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VoteLocalFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VoteLocalDetailsSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super(VoteLocalAPI, self).get_serializer_context()
        if self.action == "retrieve" and self.request.user.is_authenticated:
            context.update({"user": self.request.user})
        return context

    @action(methods=["get"], detail=False)
    def stats(self, request):
        self.filterset_class = VoteLocalStatsFilter  # TODO проверить работает ли это
        queryset = self.filter_queryset(self.get_queryset())
        votes_total_count = queryset.count()
        votes_opened_count = queryset.filter(is_opened=True).count()
        return Response(
            {
                "votes_total_count": votes_total_count,
                "votes_opened_count": votes_opened_count,
                "votes_closed_count": votes_total_count - votes_opened_count,
            }
        )

    @action(methods=["get"], detail=True)
    def locality(self, request, pk):
        instance: VoteLocal = VoteLocal.objects.get(pk=pk)
        return Response(
            LocalitySerializer(
                instance.locality.all().order_by("order", "name"), many=True
            ).data
        )

    @action(
        methods=["get"],
        detail=True,
        url_path="participants-groups",
        url_name="participants-groups",
    )
    def get_participants_groups(self, request, pk):
        """Получить список групп участников голосования"""
        instance: VoteLocal = VoteLocal.objects.get(pk=pk)
        return Response(
            LocalVotingGroupSerializer(
                instance.participants_groups.all().order_by("name"), many=True
            ).data
        )

    @action(
        methods=["patch"],
        detail=True,
        url_path="attach-groups",
        url_name="attach-groups",
    )
    def attach_groups(self, request, pk):
        """Прикрепить группу участников к голосованию"""
        instance: VoteLocal = VoteLocal.objects.get(pk=pk)
        groups_id: List[int] = dict(request.data.copy()).get("groups", [0])
        groups = LocalVotingGroup.objects.filter(pk__in=groups_id).distinct()
        [instance.participants_groups.add(group) for group in groups]
        instance.save()
        return Response(
            LocalVotingGroupSerializer(
                instance.participants_groups.all().order_by("name"), many=True
            ).data
        )

    @action(
        methods=["put"],
        detail=True,
        url_path="create-group",
        url_name="create-group",
    )
    def create_group(self, request, pk):
        """Создать группу участников и прикрепить к голосованию"""
        instance: VoteLocal = VoteLocal.objects.get(pk=pk)
        # request.method = "POST"
        # request._request.method = "POST"
        response = LocalVotingGroupAPI.as_view({"put": "create"})(request._request)
        raise ValidationError(response.data)
        group = LocalVotingGroup.objects.filter(pk=response.data.get("id")).first()
        instance.participants_groups.add(group)
        instance.save()
        return response

    @action(
        methods=["patch"],
        detail=True,
        url_path="remove-groups",
        url_name="remove-groups",
    )
    def remove_groups(self, request, pk):
        """Исключить группы участников из голосования"""
        instance: VoteLocal = VoteLocal.objects.get(pk=pk)
        groups_id: List[int] = dict(request.data.copy()).get("groups", [0])
        groups = LocalVotingGroup.objects.filter(pk__in=groups_id).distinct()
        [instance.participants_groups.remove(group) for group in groups]
        instance.save()
        return Response(
            LocalVotingGroupSerializer(
                instance.participants_groups.all().order_by("name"), many=True
            ).data
        )

    @action(
        methods=["get"],
        detail=True,
        url_path="get-urls",
        url_name="get-urls",
    )
    def get_urls(self, request, pk):
        """Получить адреса для участия по группам"""
        instance: VoteLocal = VoteLocal.objects.get(pk=pk)
        groups = instance.participants_groups.all()
        urls = []
        for group in groups:
            url = URLGenerator(instance, group)
            url.set_path_from_request(request)
            urls.append(url.get())

        return Response(urls)

    @transaction.atomic
    @action(
        methods=["post"], detail=True, permission_classes=[permissions.IsAuthenticated]
    )
    def local_vote(self, request, pk=None):
        """
        Внести вопрос+ответ по голосованию конкретного участника в таблицу "UserMunicipalVote" 
        """
        instance: VoteLocal = VoteLocal.objects.filter(pk=pk).first()
        # self._check_local_voting_permission(request, instance)
        user = request.user
        data = request.data
        self._save_user_vote(request, instance, user, data)

        # todo: Нужны ли начисления экобонусов в локальных голосованиях? Если да, то раскомментировать:
        # self._add_ecology_bonus(user, instance)
        return Response()

    @transaction.atomic
    @action(
        methods=["post"], detail=True, permission_classes=[permissions.IsAuthenticated]
    )
    def vote(self, request, pk=None):
        instance: VoteLocal = self.get_object()
        # if instance.vote_type == VoteType.LOCAL.name:
        #     raise ValidationError("wrong voting type")
        user_locality_id = request.data.pop("user_locality_id", None)
        locality = self._check_and_get_locality_from_request(user_locality_id)
        user = request.user
        data = request.data
        self._save_user_vote(request, instance, user, data, locality)

        self._add_ecology_bonus(user, instance)

        return Response()

    @classmethod
    def _check_local_voting_permission(cls, request, instance: VoteLocal) -> None:
        # if instance.vote_type != VoteType.LOCAL.name:
        #     raise ValidationError("wrong voting type")
        access_token_from_request = request.GET.copy().get("access_token")
        access_tokens_from_local_voting_group = []
        participants_groups = instance.participants_groups.all()
        if participants_groups:
            access_tokens_from_local_voting_group = [
                str(group.access_token) for group in participants_groups
            ]
        if not access_token_from_request:
            raise ValidationError("access_token is empty")
        if len(access_tokens_from_local_voting_group) == 0:
            raise ValidationError("not access_token in local_voting_group")
        if str(access_token_from_request) not in access_tokens_from_local_voting_group:
            raise ValidationError("this access_token is not suitable for voting")

    @classmethod
    def _add_ecology_bonus(cls, user: User, instance: VoteLocal) -> None:
        try:
            if user.ecology.state != UserState.INITIAL:
                EcologyUserService(user).add_bonuses_on_user_vote(instance)
        except Exception:
            pass

    @classmethod
    def _check_and_get_locality_from_request(cls, user_locality_id: int) -> Locality:
        if user_locality_id is None:
            raise ValidationError(
                "user_locality_id is empty", status.HTTP_400_BAD_REQUEST
            )

        locality = None
        try:
            locality = Locality.objects.get(pk=user_locality_id)
        except Locality.DoesNotExist:
            raise ValidationError(
                "invalid user_locality_id", status.HTTP_400_BAD_REQUEST
            )
        return locality

    @classmethod
    def _save_user_vote(
        cls,
        request,
        instance: VoteLocal,
        user: User,
        data: Dict,
        locality: Optional[Locality] = None,
    ) -> None:
        user_vote_qs = None

        # locality = data["user_locality_id"]
        # print(data, type(data))

        # if instance.multi_municipality_vote:
        #     user_vote_qs = UserMunicipalVote.objects.filter(
        #         user=user, vote=instance, locality=locality
        #     )
        # else:
        user_vote_qs = UserMunicipalVote.objects.filter(user=user, vote_loc=instance)

        # check is user already votes for locality
        if user_vote_qs.exists():
            raise ValidationError("already voted", status.HTTP_400_BAD_REQUEST)

        if locality and not instance.locality.filter(pk=locality.pk).exists():
            raise ValidationError("invalid locality", status.HTTP_400_BAD_REQUEST)

        for question in instance.local_questions.all():
            question_is_str = str(question.pk)

            if question_is_str not in data and not instance.use_question_branches:
                raise ValidationError(
                    "not all questions answered", status.HTTP_400_BAD_REQUEST
                )

            if data.get(question_is_str, None) is None:
                continue

            user_answers = list(
                map(lambda answer: AnswerDTO(**answer), data[question_is_str])
            )

            if (
                question.is_multi_answer_allowed
                and (len(user_answers) > question.max_answer_option_count)
            ) or (not question.is_multi_answer_allowed and (len(user_answers) != 1)):
                raise ValidationError(
                    "invalid answers count", status.HTTP_400_BAD_REQUEST
                )

            for answer in user_answers:

                if answer.type == AnswerType.OPTION:
                    answer_instance = None
                    try:
                        answer_instance = question.local_answers.get(pk=answer.value)
                    except VoteLocalAnswer.DoesNotExist:
                        raise ValidationError(
                            "invalid answer", status.HTTP_400_BAD_REQUEST
                        )

                    user_vote = UserMunicipalVote.objects.create(
                        user=user,
                        vote_loc=instance,
                        question_loc=question,
                        answer_loc=answer_instance,
                        locality=locality,
                    )
                    TrackUserApiMixin.create(request, user_vote, None, False)

                elif answer.type == AnswerType.CUSTOM:

                    if not question.is_custom_answer_allowed:
                        raise ValidationError(
                            "Пользовательский вариант ответа не поддерживается для этого опроса"
                        )

                    answer_instance = None
                    try:
                        answer_instance = question.local_answers.get(pk=answer.value)
                    except VoteLocalAnswer.DoesNotExist:
                        raise ValidationError(
                            "invalid answer", status.HTTP_400_BAD_REQUEST
                        )

                    user_vote = UserMunicipalVote.objects.create(
                        user=user,
                        vote_loc=instance,
                        question_loc=question,
                        answer_loc=answer_instance,
                        custom_answer=answer.text,
                        locality=locality,
                    )
                    TrackUserApiMixin.create(request, user_vote, None, False)
