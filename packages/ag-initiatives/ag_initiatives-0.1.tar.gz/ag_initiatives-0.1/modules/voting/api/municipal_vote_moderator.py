from django.db import transaction
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.models import Category
from modules.core.permissions import IsModerator
from modules.voting.api.filters import VoteMunicipalFilter
from modules.voting.api.serializers import (
    MunicipalVoteListSerializer,
    CategoryDetailsSerializer,
    MunicipalVoteUpdateSerializer,
    LocalityDetailsSerializer,
    MunicipalVoteDetailsSerializer,
    MunicipalVoteUpdateQuestionSerializer,
    MunicipalVoteCreateQuestionSerializer,
    MunicipalVoteUpdateAnswerSerializer,
    MunicipalVoteCreateAnswerSerializer,
)

from modules.voting.models import (
    VoteMunicipal,
    VoteState,
    VoteMunicipalQuestion,
    VoteMunicipalAnswer,
    RejectReason,
)
from django_filters import rest_framework as filters

from modules.voting.services.mail_service import MailService


class MunicipalVoteModeratorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        VoteMunicipal.objects.filter(state__in=[VoteState.CREATED])
        .order_by("-to_moderation_date")
        .prefetch_related(
            Prefetch("municipal_questions", queryset=VoteMunicipalQuestion.objects.order_by("order")),
            Prefetch(
                "municipal_questions__municipal_answers",
                queryset=VoteMunicipalAnswer.objects.order_by("order"),
            ),
        )
    )
    serializer_class = MunicipalVoteListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VoteMunicipalFilter
    permission_classes = [IsModerator]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MunicipalVoteDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk):
        instance: VoteMunicipal = self.get_object()

        if instance.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.moderator_accept()
        instance.save(update_fields=["state", "moderation_date"])

        MailService.notify_operator__moderation_accepted(instance)

        return Response(
            MunicipalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: VoteMunicipal = self.get_object()

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
            MunicipalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=False)
    def reject_reasons(self, request):
        return Response(
            [m.text for m in RejectReason.objects.all()], status=status.HTTP_200_OK
        )

    @action(methods=["get"], detail=True)
    def categories(self, request, pk):
        instance: VoteMunicipal = self.get_object()
        return Response(
            CategoryDetailsSerializer(Category.objects.all(), many=True).data
        )

    @action(methods=["get"], detail=True)
    def localities(self, request, pk):
        instance: VoteMunicipal = self.get_object()
        return Response(
            LocalityDetailsSerializer(
                instance.department.locality.all().order_by("order", "name"), many=True
            ).data
        )

    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="municipal-update-details")
    def update_details(self, request, pk):
        vote: VoteMunicipal = self.get_object()

        if request.method == "GET":
            return Response(
                MunicipalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
            )

        if vote.state != VoteState.CREATED:
            return Response(
                'Голосование не в статусе "На модерации"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = MunicipalVoteUpdateSerializer(instance=vote, data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.get("locality")

        if not all(elem in vote.department.locality.all() for elem in vote_localities):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions_data = vote_data.pop("municipal_questions", None)

        vote = serializer.save()

        questions: list = []
        for question_data in questions_data:
            answers_data = question_data.pop("municipal_answers", None)

            question_id = question_data.get("id", None)

            question_serializer = (
                MunicipalVoteUpdateQuestionSerializer(
                    instance=VoteMunicipalQuestion.objects.get(pk=question_id),
                    data=question_data,
                )
                if question_id
                else MunicipalVoteCreateQuestionSerializer(data=question_data)
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
                    MunicipalVoteUpdateAnswerSerializer(
                        instance=VoteMunicipalAnswer.objects.get(pk=answer_id),
                        data=answer_data,
                    )
                    if answer_id
                    else MunicipalVoteCreateAnswerSerializer(data=answer_data)
                )

                answer_serializer.is_valid(raise_exception=True)
                answer = answer_serializer.save(vote_question=question)
                answers.append(answer)

            question.municipal_answers.exclude(id__in=[m.pk for m in answers]).delete()
            question.municipal_answers.set(answers)

        vote.municipal_questions.exclude(id__in=[m.pk for m in questions]).delete()
        vote.municipal_questions.set(questions)

        return Response(
            MunicipalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
        )
