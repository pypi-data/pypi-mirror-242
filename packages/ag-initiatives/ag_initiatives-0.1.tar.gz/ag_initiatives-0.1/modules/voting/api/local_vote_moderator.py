from django.db import transaction
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.models import Category
from modules.core.permissions import IsModerator
from modules.voting.api.filters import VoteLocalFilter
from modules.voting.api.serializers import (
    CategoryDetailsSerializer,
    LocalityDetailsSerializer,
    LocalVoteUpdateSerializer,
    LocalVoteListSerializer,
    LocalVoteDetailsSerializer,
    LocalVoteUpdateQuestionSerializer,
    LocalVoteCreateQuestionSerializer,
    LocalVoteUpdateAnswerSerializer,
    LocalVoteCreateAnswerSerializer,
)

from modules.voting.models import (
    VoteLocal,
    VoteState,
    VoteLocalQuestion,
    VoteLocalAnswer,
    RejectReason,
)
from django_filters import rest_framework as filters

from modules.voting.services.mail_service import MailService


class LocalVoteModeratorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        VoteLocal.objects.filter(state__in=[VoteState.CREATED])
        .order_by("-to_moderation_date")
        .prefetch_related(
            Prefetch("local_questions", queryset=VoteLocalQuestion.objects.order_by("order")),
            Prefetch(
                "local_questions__local_answers",
                queryset=VoteLocalAnswer.objects.order_by("order"),
            ),
        )
    )
    serializer_class = LocalVoteListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VoteLocalFilter
    permission_classes = [IsModerator]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LocalVoteDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk):
        instance: VoteLocal = self.get_object()

        if instance.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.moderator_accept()
        instance.save(update_fields=["state", "moderation_date"])

        MailService.notify_operator__moderation_accepted(instance)

        return Response(
            LocalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: VoteLocal = self.get_object()

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
            LocalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=False)
    def reject_reasons(self, request):
        return Response(
            [m.text for m in RejectReason.objects.all()], status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=True)
    def categories(self, request, pk):
        instance: VoteLocal = self.get_object()
        return Response(
            CategoryDetailsSerializer(Category.objects.all(), many=True).data
        )

    @action(methods=["get"], detail=True)
    def localities(self, request, pk):
        instance: VoteLocal = self.get_object()
        return Response(
            LocalityDetailsSerializer(
                instance.department.locality.all().order_by("order", "name"), many=True
            ).data
        )

    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="Local-update-details")
    def update_details(self, request, pk):
        vote: VoteLocal = self.get_object()

        if request.method == "GET":
            return Response(
                LocalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
            )

        if vote.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = LocalVoteUpdateSerializer(instance=vote, data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.get("locality")

        if not all(elem in vote.department.locality.all() for elem in vote_localities):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions_data = vote_data.pop("local_questions", None)

        vote = serializer.save()

        questions: list = []
        for question_data in questions_data:
            answers_data = question_data.pop("local_answers", None)

            question_id = question_data.get("id", None)

            question_serializer = (
                LocalVoteUpdateQuestionSerializer(
                    instance=VoteLocalQuestion.objects.get(pk=question_id),
                    data=question_data,
                )
                if question_id
                else LocalVoteCreateQuestionSerializer(data=question_data)
            )

            question_serializer.is_valid(raise_exception=True)
            question = question_serializer.save(vote=vote)
            questions.append(question)

            answers = []

            for answer_data in answers_data:
                answer_id = answer_data.get("id", None)

                answer_image = answer_data.pop("image", None)
                if answer_image:
                    answer_data["image"] = answer_image.pk

                answer_serializer = (
                    LocalVoteUpdateAnswerSerializer(
                        instance=VoteLocalAnswer.objects.get(pk=answer_id),
                        data=answer_data,
                    )
                    if answer_id
                    else LocalVoteCreateAnswerSerializer(data=answer_data)
                )

                answer_serializer.is_valid(raise_exception=True)
                answer = answer_serializer.save(vote_question=question)
                answers.append(answer)

            question.local_answers.exclude(id__in=[m.pk for m in answers]).delete()
            question.local_answers.set(answers)

        vote.local_questions.exclude(id__in=[m.pk for m in questions]).delete()
        vote.local_questions.set(questions)

        return Response(
            LocalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
        )
