from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch, Q, Subquery, BooleanField
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.models import Category
from modules.core.permissions import IsModerator
from modules.voting.api.filters import VoteFilter
from modules.voting.api.serializers import (
    VoteModeratorListSerializer,
    CategoryDetailsSerializer,
    LocalityDetailsSerializer,
    VoteModeratorDetailsSerializer,
    VoteModeratorUpdateQuestionSerializer,
    VoteModeratorCreateQuestionSerializer,
    VoteModeratorUpdateAnswerOptionSerializer,
    VoteModeratorCreateAnswerOptionSerializer,
)
from modules.voting.api.serializers import VoteModeratorUpdateSerializer
from modules.voting.models import (
    Vote,
    VoteState,
    VoteQuestion,
    VoteAnswerOption,
    RejectReason,
)
from django_filters import rest_framework as filters

from modules.voting.services.mail_service import MailService


class VoteModeratorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Vote.objects.filter(state__in=[VoteState.CREATED])
        .order_by("-to_moderation_date")
        .prefetch_related(
            Prefetch("questions", queryset=VoteQuestion.objects.order_by("order")),
            Prefetch(
                "questions__answers",
                queryset=VoteAnswerOption.objects.order_by("order"),
            ),
        ).distinct()
    )
    serializer_class = VoteModeratorListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VoteFilter
    permission_classes = [IsModerator]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VoteModeratorDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk):
        instance: Vote = self.get_object()

        if instance.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.moderator_accept()
        instance.save(update_fields=["state", "moderation_date"])

        MailService.notify_operator__moderation_accepted(instance)

        return Response(
            VoteModeratorDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: Vote = self.get_object()

        if instance.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason_text = request.data.get("reason_text", "")
        reason_text_comment = request.data.get("reason_text_comment", "")

        if len(reason_text) == 0 and len(reason_text_comment) == 0:
            return Response(
                "Не указана причина отказа", status=status.HTTP_400_BAD_REQUEST
            )

        instance.reject_reason_text = reason_text
        instance.reject_reason_text_comment = reason_text_comment

        instance.moderator_reject()
        instance.save(
            update_fields=[
                "state",
                "moderation_date",
                "reject_reason_text",
                "reject_reason_text_comment",
            ]
        )

        MailService.notify_operator__moderation_rejected(instance)

        return Response(
            VoteModeratorDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=False)
    def reject_reasons(self, request):
        return Response(
            [m.text for m in RejectReason.objects.all()], status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=True)
    def categories(self, request, pk):
        return Response(
            CategoryDetailsSerializer(Category.objects.all(), many=True).data
        )

    @action(methods=["get"], detail=True)
    def localities(self, request, pk):
        instance: Vote = self.get_object()
        if not instance.department:
            return Response(data=[])
        return Response(
            LocalityDetailsSerializer(
                instance.department.locality.all().order_by("order", "name"), many=True
            ).data
        )

    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="update-details")
    def update_details(self, request, pk):
        vote: Vote = self.get_object()
        questions_data = request.data.pop("questions", None)

        if request.method == "GET":
            return Response(
                VoteModeratorUpdateSerializer(vote).data, status=status.HTTP_200_OK
            )

        if vote.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = VoteModeratorUpdateSerializer(instance=vote, data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.get("locality")

        if vote.author and vote.author.is_operator:
            allowed_localities = vote.author.sub_permissions.operator_permissions.voting_localities.all()
        elif vote.department:
            allowed_localities = vote.department.locality.all()
        else:
            allowed_localities = []

        if not all(elem in allowed_localities for elem in vote_localities):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        vote = serializer.save()

        questions: list = []
        for question_data in questions_data:
            answers_data = question_data.pop("answers", None)

            question_id = question_data.get("id", None)

            question_serializer = (
                VoteModeratorUpdateQuestionSerializer(
                    instance=VoteQuestion.objects.get(pk=question_id),
                    data=question_data,
                )
                if question_id
                else VoteModeratorCreateQuestionSerializer(data=question_data)
            )

            question_serializer.is_valid(raise_exception=True)
            question = question_serializer.save(vote=vote)
            questions.append(question)

            answers: list = []
            for answer_data in answers_data:
                answer_id = answer_data.get("id", None)

                answer_serializer = (
                    VoteModeratorUpdateAnswerOptionSerializer(
                        instance=VoteAnswerOption.objects.get(pk=answer_id),
                        data=answer_data,
                    )
                    if answer_id
                    else VoteModeratorCreateAnswerOptionSerializer(data=answer_data)
                )

                answer_serializer.is_valid(raise_exception=True)
                answer = answer_serializer.save(vote_question=question)
                answers.append(answer)

            question.answers.exclude(id__in=[m.pk for m in answers]).delete()
            question.answers.set(answers)

        vote.questions.exclude(id__in=[m.pk for m in questions]).delete()
        vote.questions.set(questions)

        return Response(
            VoteModeratorUpdateSerializer(vote).data, status=status.HTTP_200_OK
        )
