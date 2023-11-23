from django.db import transaction
from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from modules.core.permissions import IsOperator

from modules.voting.api.filters import VoteMunicipalFilter
from modules.core.models import Category

from modules.voting.api.serializers import (
    MunicipalVoteListSerializer,
    CategoryDetailsSerializer,
    LocalityDetailsSerializer,
    MunicipalVoteDetailsSerializer,
    MunicipalVoteCreateSerializer,
    MunicipalVoteUpdateSerializer,
    MunicipalVoteUpdateQuestionSerializer,
    MunicipalVoteCreateQuestionSerializer,
    MunicipalVoteUpdateAnswerSerializer,
    MunicipalVoteCreateAnswerSerializer,
)
from modules.voting.models.vote import Vote

from modules.voting.services.mail_service import MailService
from modules.voting.models import VoteMunicipal, VoteState, VoteMunicipalQuestion, VoteMunicipalAnswer


class MunicipalVoteOperatorLKOAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        VoteMunicipal.objects.all()
        .order_by("-creation_date")
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
    permission_classes = [IsOperator]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MunicipalVoteDetailsSerializer
        # return super().get_serializer_class()
        return self.serializer_class

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    # def get_queryset(self):
    #     return super().get_queryset().filter(department=self.request.user.department)
    def get_queryset(self):
        return self.queryset.filter(department=self.request.user.department)

    @action(methods=["get"], detail=False)
    def categories(self, request):
        return Response(
            CategoryDetailsSerializer(Category.objects.all(), many=True).data
        )

    @action(methods=["get"], detail=False)
    def localities(self, request):
        return Response(
            LocalityDetailsSerializer(
                request.user.department.locality.all().order_by("order", "name"),
                many=True,
            ).data
        )
    
    @transaction.atomic
    @action(methods=["post"], detail=False)
    def add(self, request):
        serializer = MunicipalVoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.pop("locality")
        vote_municipalities = vote_data.pop("municipal_formation")
        vote_categories = vote_data.pop("vote_category")
        
        if not all(
            elem in request.user.department.locality.all() for elem in vote_localities
        ):
            return Response(
                "Некорректный населенный пункт",
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        questions = vote_data.pop("questions", None)

        vote = VoteMunicipal.objects.create(
            **vote_data,
            state=VoteState.DRAFT,
            department=request.user.department,
        )

        vote.locality.add(*vote_localities)
        vote.municipal_formation.add(*vote_municipalities)
        vote.vote_category.add(*vote_categories)

        for question_data in questions:
            answers = question_data.pop("municipal_answers", None)
            question = VoteMunicipalQuestion.objects.create(
                **question_data,
                vote=vote,
            )

            if answers:
                if question.max_answer_option_count > len(answers):
                    raise ValidationError(
                        "Максимальное количество вариантов ответов больше чем вариантов ответов."
                    )

                for answer_data in answers:
                    VoteMunicipalAnswer.objects.create(
                        **answer_data,
                        vote_question=question,
                    )
        vote: VoteMunicipal
        MailService.notify_moderator__vote_created(vote=vote)

        data = MunicipalVoteDetailsSerializer(vote).data

        return Response(
            data=data, 
            status=status.HTTP_201_CREATED,
        )


    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="update-details")
    def update_details(self, request, pk):
        vote: VoteMunicipal = self.get_object()

        if request.method == "GET":
            return Response(
                MunicipalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
            )

        if vote.state != VoteState.DRAFT:
            return Response(
                'Голосование не в статусе "Черновик"',
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = MunicipalVoteUpdateSerializer(instance=vote, data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data
 
        vote_localities = vote_data.get("locality")

        if not all(
            elem in request.user.department.locality.all() for elem in vote_localities
        ):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions_data = vote_data.pop("municipal_questions", None)
        
        vote = serializer.save()

        questions = []

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

            if question.max_answer_option_count > len(answers):
                raise ValidationError(
                    "Максимальное количество вариантов ответов больше чем вариантов ответов."
                )

            question.municipal_answers.exclude(id__in=[m.pk for m in answers]).delete()
            question.municipal_answers.set(answers)
        
        vote.municipal_questions.exclude(id__in=[m.pk for m in questions]).delete()
        vote.municipal_questions.set(questions)

        return Response(
            MunicipalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
        )


    @transaction.atomic
    @action(methods=["get"], detail=True)
    def to_moderation(self, request, pk):
        instance: VoteMunicipal = self.get_object()

        if instance.state != VoteState.DRAFT:
            return Response(
                'Голосование не в статусе "Черновик"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.operator_to_moderation()
        instance.save(update_fields=["state", "to_moderation_date"])

        return Response(
            MunicipalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )


    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk):
        instance: VoteMunicipal = self.get_object()

        if instance.state != VoteState.MODERATION_ACCEPTED:
            return Response(
                'Голосование не в статусе "Одобрен модератором"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.operator_accept()
        instance.save(update_fields=["state", "operator_action_date"])

        return Response(
            MunicipalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: VoteMunicipal = self.get_object()

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
            MunicipalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )
