import collections
import logging
from typing import Union, List, Optional, Dict

from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch, Q, BooleanField, Subquery
from django_filters import rest_framework as filters
from pydantic import BaseModel, validator
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from django.http.request import HttpRequest

from modules.api.filters import VoteFilter, VoteStatsFilter
from modules.api.serializers import (
    VoteSerializer,
    VoteDetailsSerializer,
    LocalitySerializer,
)
from modules.core.mixins.user_track_admin import TrackUserApiMixin
from modules.core.models import Locality, User
from modules.ecology.models import UserState
from modules.voting.api import LocalVotingGroupAPI
from modules.voting.api.serializers import LocalVotingGroupSerializer
from modules.voting.enums import VoteType
from modules.voting.models import (
    VoteState,
    Vote,
    UserVote,
    VoteQuestion,
    VoteAnswerOption,
    LocalVotingGroup,
)

from modules.ecology.services.user_service import UserService as EcologyUserService
from modules.voting.services import URLGenerator


class AnswerType:
    OPTION = "OPTION"
    CUSTOM = "CUSTOM"

    RESOLVER = collections.OrderedDict(
        [(OPTION, "Выбор"), (CUSTOM, "Вариант пользователя")]
    )


class AnswerDTO(BaseModel):
    value: int
    type: str
    text: Optional[str]

    @validator("type")
    def validate_type(cls, value):
        if value not in AnswerType.RESOLVER.keys():
            raise ValidationError("invalid answer type")
        return value


class VoteAPI(viewsets.ReadOnlyModelViewSet):
    serializer_class = VoteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VoteFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = (
            Vote.objects.filter(is_published=True)
            .prefetch_related(
                Prefetch("questions", queryset=VoteQuestion.objects.order_by("order")),
                Prefetch(
                    "questions__answers",
                    queryset=VoteAnswerOption.objects.order_by("order"),
                ),
            )
            .order_by("-start_date").distinct()
        )
        user = self.request.user
        if user.is_authenticated:
            if age := user.age:
                age_restriction_filter = Q(type_publication_with_age_restriction=True) & (
                    Q(age_restriction_start__lte=age) & Q(age_restriction_finish__gt=age)
                )
            else:
                age_restriction_filter = Q()

            category_filter = Q(type_publication_with_group_restriction=True) & (
                Q(participants_categories__id__in=user.categories.values_list("id", flat=True)) |
                Q(participants_categories__isnull=True)
            )

            queryset = queryset.filter(
                (Q(type_publication_with_age_restriction=False) | age_restriction_filter) &
                (Q(type_publication_with_group_restriction=False) | category_filter)
            ).distinct()
        else:
            queryset = queryset.filter(
                Q(type_publication_with_age_restriction=False) & Q(type_publication_with_group_restriction=False)
            ).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VoteDetailsSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super(VoteAPI, self).get_serializer_context()
        if self.action == "retrieve" and self.request.user.is_authenticated:
            context.update({"user": self.request.user})
        return context

    @action(methods=["get"], detail=False)
    def stats(self, request):
        self.filterset_class = VoteStatsFilter  # TODO проверить работает ли это
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
        instance: Vote = Vote.objects.get(pk=pk)
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
        instance: Vote = Vote.objects.get(pk=pk)
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
        instance: Vote = Vote.objects.get(pk=pk)
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
        instance: Vote = Vote.objects.get(pk=pk)
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
        instance: Vote = Vote.objects.get(pk=pk)
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
        instance: Vote = Vote.objects.get(pk=pk)
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
        instance: Vote = Vote.objects.filter(pk=pk).first()
        self._check_local_voting_permission(request, instance)
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
        instance: Vote = self.get_object()
        user_locality_id = request.data.pop("user_locality_id", None)
        locality = self._check_and_get_locality_from_request(user_locality_id)
        user = request.user
        data = request.data
        self._save_user_vote(request, instance, user, data, locality)

        # user_vote_qs = None
        #
        # if instance.multi_locality_vote:
        #     user_vote_qs = UserVote.objects.filter(
        #         user=user, vote=instance, locality=locality
        #     )
        # else:
        #     user_vote_qs = UserVote.objects.filter(user=user, vote=instance)
        #
        # # check is user already votes for locality
        # if user_vote_qs.exists():
        #     raise ValidationError("already voted", status.HTTP_400_BAD_REQUEST)
        #
        # if not instance.locality.filter(pk=locality.pk).exists():
        #     raise ValidationError("invalid locality", status.HTTP_400_BAD_REQUEST)
        #
        # for question in instance.questions.all():
        #     question_is_str = str(question.pk)
        #
        #     if (
        #         question_is_str not in request.data
        #         and not instance.use_question_branches
        #     ):
        #         raise ValidationError(
        #             "not all questions answered", status.HTTP_400_BAD_REQUEST
        #         )
        #
        #     if request.data.get(question_is_str, None) is None:
        #         continue
        #
        #     user_answers = list(
        #         map(lambda answer: AnswerDTO(**answer), request.data[question_is_str])
        #     )
        #
        #     if (
        #         question.is_multi_answer_allowed
        #         and (len(user_answers) > question.max_answer_option_count)
        #     ) or (not question.is_multi_answer_allowed and (len(user_answers) != 1)):
        #         raise ValidationError(
        #             "invalid answers count", status.HTTP_400_BAD_REQUEST
        #         )
        #
        #     for answer in user_answers:
        #
        #         if answer.type == AnswerType.OPTION:
        #             answer_instance = None
        #             try:
        #                 answer_instance = question.answers.get(pk=answer.value)
        #             except VoteAnswerOption.DoesNotExist:
        #                 raise ValidationError(
        #                     "invalid answer", status.HTTP_400_BAD_REQUEST
        #                 )
        #
        #             user_vote = UserVote.objects.create(
        #                 user=user,
        #                 vote=instance,
        #                 question=question,
        #                 answer_option=answer_instance,
        #                 locality=locality,
        #             )
        #             TrackUserApiMixin.create(request, user_vote, None, False)
        #
        #         elif answer.type == AnswerType.CUSTOM:
        #
        #             if not question.is_custom_answer_allowed:
        #                 raise ValidationError(
        #                     "Пользовательский вариант ответа не поддерживается для этого опроса"
        #                 )
        #
        #             answer_instance = None
        #             try:
        #                 answer_instance = question.answers.get(pk=answer.value)
        #             except VoteAnswerOption.DoesNotExist:
        #                 raise ValidationError(
        #                     "invalid answer", status.HTTP_400_BAD_REQUEST
        #                 )
        #
        #             user_vote = UserVote.objects.create(
        #                 user=user,
        #                 vote=instance,
        #                 question=question,
        #                 answer_option=answer_instance,
        #                 custom_answer=answer.text,
        #                 locality=locality,
        #             )
        #             TrackUserApiMixin.create(request, user_vote, None, False)

        # Добавляем бонусы в модуле экология

        self._add_ecology_bonus(user, instance)

        return Response()

    @classmethod
    def _check_local_voting_permission(cls, request, instance: Vote) -> None:
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
    def _add_ecology_bonus(cls, user: User, instance: Vote) -> None:
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
        instance: Vote,
        user: User,
        data: Dict,
        locality: Optional[Locality] = None,
    ) -> None:
        user_vote_qs = None

        if instance.multi_locality_vote:
            user_vote_qs = UserVote.objects.filter(
                user=user, vote=instance, locality=locality
            )
        else:
            user_vote_qs = UserVote.objects.filter(user=user, vote=instance)

        # check is user already votes for locality
        if user_vote_qs.exists():
            raise ValidationError("already voted", status.HTTP_400_BAD_REQUEST)

        if locality and not instance.locality.filter(pk=locality.pk).exists():
            raise ValidationError("invalid locality", status.HTTP_400_BAD_REQUEST)

        if any(question.use_question_branches for question in instance.questions.all()):
            questions = []
            answers = []
            next_question_order = 0
            while next_question_order is not None and len(questions) < instance.questions.all().count():
                question = instance.questions.all().filter(order=next_question_order).first()
                questions.append(question)
                chosen_answer_id = data.get(str(question.id), None)
                if chosen_answer_id:
                    chosen_answer_id = chosen_answer_id[0]["value"]
                    chosen_answer = VoteAnswerOption.objects.filter(pk=chosen_answer_id).first()
                    if chosen_answer:
                        next_question_order = chosen_answer.next_question_order
                        answers.append(chosen_answer)
            if len(questions) != len(answers):
                raise ValidationError(
                    "not all questions answered", status.HTTP_400_BAD_REQUEST
                )
        for question in instance.questions.all():
            question_is_str = str(question.pk)

            if not(any(question.use_question_branches for question in instance.questions.all())):
                if question_is_str not in data:
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
                        answer_instance = question.answers.get(pk=answer.value)
                    except VoteAnswerOption.DoesNotExist:
                        raise ValidationError(
                            "invalid answer", status.HTTP_400_BAD_REQUEST
                        )

                    user_vote = UserVote.objects.create(
                        user=user,
                        vote=instance,
                        question=question,
                        answer_option=answer_instance,
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
                        answer_instance = question.answers.get(pk=answer.value)
                    except VoteAnswerOption.DoesNotExist:
                        raise ValidationError(
                            "invalid answer", status.HTTP_400_BAD_REQUEST
                        )

                    user_vote = UserVote.objects.create(
                        user=user,
                        vote=instance,
                        question=question,
                        answer_option=answer_instance,
                        custom_answer=answer.text,
                        locality=locality,
                    )
                    TrackUserApiMixin.create(request, user_vote, None, False)
