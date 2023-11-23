from django.db import transaction
from django.db.models import Prefetch
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.core.models import Category
from modules.core.permissions import IsOperator
from modules.voting.api.filters import VoteFilter
from modules.voting.api.serializers import (
    VoteOperatorListSerializer,
    CategoryDetailsSerializer,
    LocalityDetailsSerializer,
    VoteOperatorDetailsSerializer,
    VoteOperatorUpdateSerializer,
    VoteOperatorUpdateQuestionSerializer,
)
from modules.voting.api.serializers import VoteOperatorCreateSerializer
from modules.voting.api.serializers.vote_operator import (
    VoteOperatorCreateQuestionSerializer,
    VoteOperatorUpdateAnswerOptionSerializer,
    VoteOperatorCreateAnswerOptionSerializer,
)
from modules.voting.models import Vote, VoteState, VoteQuestion, VoteAnswerOption
from django_filters import rest_framework as filters

from modules.voting.services.mail_service import MailService


class VoteOperatorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Vote.objects.all()
        .order_by("-creation_date")
        .prefetch_related(
            Prefetch("questions", queryset=VoteQuestion.objects.order_by("order")),
            Prefetch(
                "questions__answers",
                queryset=VoteAnswerOption.objects.order_by("order"),
            ),
        )
    )
    serializer_class = VoteOperatorListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VoteFilter
    permission_classes = [IsOperator]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return VoteOperatorDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    def get_queryset(self):
        return super().get_queryset().filter(
            department=self.request.user.sub_permissions.operator_permissions.department)

    @action(methods=["get"], detail=False)
    def categories(self, request):
        return Response(
            CategoryDetailsSerializer(request.user.sub_permissions.operator_permissions.voting_categories.all(),
                                      many=True).data
        )

    @action(methods=["get"], detail=False)
    def localities(self, request):
        return Response(
            LocalityDetailsSerializer(
                request.user.sub_permissions.operator_permissions.voting_localities.all().order_by("order", "name"),
                many=True,
            ).data
        )

    @transaction.atomic
    @action(methods=["post"], detail=False)
    def add(self, request):
        vote_id = request.data.pop("id", None)
        vote_old = Vote.objects.filter(pk=vote_id).first()

        serializer = VoteOperatorCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.pop("locality")
        participants_categories = vote_data.pop("participants_categories", None)

        operator_localities = all(elem in request.user.sub_permissions.operator_permissions.voting_localities.all()
                                  for elem in vote_localities)
        vote_old_localities = all(elem in vote_old.locality.all() for elem in vote_localities) if vote_old else None
        if not operator_localities and not vote_old_localities:
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions = vote_data.pop("questions", None)

        vote = Vote.objects.create(
            **vote_data,
            state=VoteState.DRAFT,
            department=request.user.sub_permissions.operator_permissions.department,
        )
        vote.locality.add(*vote_localities)
        if participants_categories:
            vote.participants_categories.set(
                participants_categories)

        for question_data in questions:
            answers = question_data.pop("answers", None)
            question = VoteQuestion.objects.create(
                **question_data,
                vote=vote,
            )

            if answers:
                if question.max_answer_option_count > len(answers):
                    raise ValidationError(
                        "Максимальное количество вариантов ответов больше чем вариантов ответов."
                    )

                for answer_data in answers:
                    VoteAnswerOption.objects.create(
                        **answer_data,
                        vote_question=question,
                    )

        MailService.notify_moderator__vote_created(vote=vote)

        return Response(
            VoteOperatorDetailsSerializer(vote).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="update-details")
    def update_details(self, request, pk):
        vote: Vote = self.get_object()
        questions_data = request.data.pop("questions", None)

        if request.method == "GET":
            return Response(
                VoteOperatorUpdateSerializer(vote).data, status=status.HTTP_200_OK
            )

        if vote.state != VoteState.DRAFT:
            return Response(
                'Голосование не в статусе "Черновик"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = VoteOperatorUpdateSerializer(instance=vote, data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.get("locality")

        if not all(elem in request.user.sub_permissions.operator_permissions.voting_localities.all()
                   for elem in vote_localities):
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
                VoteOperatorUpdateQuestionSerializer(
                    instance=VoteQuestion.objects.get(pk=question_id),
                    data=question_data,
                )
                if question_id
                else VoteOperatorCreateQuestionSerializer(data=question_data)
            )

            question_serializer.is_valid(raise_exception=True)
            question = question_serializer.save(vote=vote)
            questions.append(question)

            answers: list = []
            for answer_data in answers_data:
                answer_id = answer_data.get("id", None)

                answer_serializer = (
                    VoteOperatorUpdateAnswerOptionSerializer(
                        instance=VoteAnswerOption.objects.get(pk=answer_id),
                        data=answer_data,
                    )
                    if answer_id
                    else VoteOperatorCreateAnswerOptionSerializer(data=answer_data)
                )

                answer_serializer.is_valid(raise_exception=True)
                answer = answer_serializer.save(vote_question=question)
                answers.append(answer)

            if question.max_answer_option_count > len(answers):
                raise ValidationError(
                    "Максимальное количество вариантов ответов больше чем вариантов ответов."
                )

            question.answers.exclude(id__in=[m.pk for m in answers]).delete()
            question.answers.set(answers)

        vote.questions.exclude(id__in=[m.pk for m in questions]).delete()
        vote.questions.set(questions)

        return Response(
            VoteOperatorUpdateSerializer(vote).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["get"], detail=True)
    def to_moderation(self, request, pk):
        instance: Vote = self.get_object()

        if instance.state != VoteState.DRAFT:
            return Response(
                'Голосование не в статусе "Черновик"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.operator_to_moderation()
        instance.save(update_fields=["state", "to_moderation_date"])

        return Response(
            VoteOperatorDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk):
        instance: Vote = self.get_object()

        if instance.state != VoteState.MODERATION_ACCEPTED:
            return Response(
                'Голосование не в статусе "Одобрен модератором"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.operator_accept()
        instance.save(update_fields=["state", "operator_action_date"])

        return Response(
            VoteOperatorDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def copy(self, request, pk):
        instance: Vote = self.get_object()
        instance.id = None
        # for locality in instance.locality.all():
        #     locality.id = None
        serializer = VoteOperatorCreateSerializer(data=instance)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data
        vote_localities = vote_data.pop("locality")

        if not all(
                elem in request.user.department.locality.all() for elem in vote_localities
        ):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions = vote_data.pop("questions", None)

        vote = Vote.objects.create(
            **vote_data,
            state=VoteState.DRAFT,
            department=request.user.department,
        )
        vote.locality.add(*vote_localities)

        for question_data in questions:
            answers = question_data.pop("answers", None)
            question = VoteQuestion.objects.create(
                **question_data,
                vote=vote,
            )

            if answers:
                if question.max_answer_option_count > len(answers):
                    raise ValidationError(
                        "Максимальное количество вариантов ответов больше чем вариантов ответов."
                    )

                for answer_data in answers:
                    VoteAnswerOption.objects.create(
                        **answer_data,
                        vote_question=question,
                    )

        MailService.notify_moderator__vote_created(vote=vote)

        return Response(
            VoteOperatorDetailsSerializer(vote).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: Vote = self.get_object()

        if instance.state != VoteState.MODERATION_ACCEPTED:
            return Response(
                'Голосование не в статусе "Одобрен модератором"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason_text = request.data.get("reason_text", "")

        if len(reason_text) == 0:
            return Response(
                "Не указана причина отказа", status=status.HTTP_400_BAD_REQUEST
            )

        instance.operator_reject_reason_text = reason_text

        instance.operator_reject()
        instance.save(
            update_fields=[
                "state",
                "operator_action_date",
                "operator_reject_reason_text",
            ]
        )

        return Response(
            VoteOperatorDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )
