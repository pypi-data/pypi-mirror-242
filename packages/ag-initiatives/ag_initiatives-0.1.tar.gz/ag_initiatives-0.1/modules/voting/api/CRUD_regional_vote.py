from traceback import print_tb
from django.db import transaction
from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from modules.core.permissions import IsOperatorLKOMulti

from modules.voting.api.filters import VoteRegionalFilter
from modules.core.models import Category

from modules.voting.api.serializers import (
    RegionalVoteListSerializer,
    CategoryDetailsSerializer,
    RegionalVoteDetailsSerializer,
    RegionalVoteCreateSerializer,
    RegionalVoteUpdateSerializer,
    RegionalVoteUpdateQuestionSerializer,
    RegionalVoteCreateQuestionSerializer,
    RegionalVoteUpdateAnswerSerializer,
    RegionalVoteCreateAnswerSerializer,
)

from modules.voting.services.mail_service import MailService
from modules.voting.models import VoteRegional, VoteState, VoteRegionalQuestion, VoteRegionalAnswer


class RegionalVoteOperatorLKOAPI(viewsets.ReadOnlyModelViewSet):
    queryset = (
        VoteRegional.objects.all()
        .order_by("-creation_date")
        .prefetch_related(
            Prefetch("regional_questions", queryset=VoteRegionalQuestion.objects.order_by("order")),
            Prefetch(
                "regional_questions__regional_answers",
                queryset=VoteRegionalAnswer.objects.order_by("order"),
            ),
        )
    )
    serializer_class = RegionalVoteListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = VoteRegionalFilter
    permission_classes = [IsOperatorLKOMulti]
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RegionalVoteDetailsSerializer
        return self.serializer_class

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    def get_queryset(self):
        return self.queryset.filter(department=self.request.user.department)

    @action(methods=["get"], detail=False)
    def categories(self, request):
        return Response(
            CategoryDetailsSerializer(Category.objects.all(), many=True).data
        )

    # @action(methods=["get"], detail=False)
    # def localities(self, request):
    #     return Response(
    #         LocalityDetailsSerializer(
    #             request.user.department.locality.all().order_by("order", "name"),
    #             many=True,
    #         ).data
    #     )
    
    @transaction.atomic
    @action(methods=["post"], detail=False)
    def add(self, request):

        serializer = RegionalVoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_municipalities = vote_data.pop("municipal_formation")
        try:
            vote_categories = vote_data.pop("vote_category")
        except KeyError:
            vote_categories = []
        questions = vote_data.pop("questions", None)

        vote = VoteRegional.objects.create(
            **vote_data,
            state=VoteState.DRAFT,
            department=request.user.department,
        )

        vote.municipal_formation.add(*vote_municipalities)
        vote.vote_category.add(*vote_categories)

        for question_data in questions:
            answers = question_data.pop("regional_answers", None)
            question = VoteRegionalQuestion.objects.create(
                **question_data,
                vote=vote,
            )

            if answers:
                if question.max_answer_option_count > len(answers):
                    raise ValidationError(
                        "Максимальное количество вариантов ответов больше чем вариантов ответов."
                    )

                for answer_data in answers:
                    VoteRegionalAnswer.objects.create(
                        **answer_data,
                        vote_question=question,
                    )
        vote: VoteRegional
        MailService.notify_moderator__vote_created(vote=vote)

        data = RegionalVoteDetailsSerializer(vote).data

        return Response(
            data=data, 
            status=status.HTTP_201_CREATED,
        )


    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="update-details")
    def update_details(self, request, pk):
        vote: VoteRegional = self.get_object()

        if request.method == "GET":
            return Response(
                RegionalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
            )

        if vote.state != VoteState.DRAFT:
            return Response(
                'Голосование не в статусе "Черновик"',
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        serializer = RegionalVoteUpdateSerializer(instance=vote, data=request.data)
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data
 
        # vote_municipaties = vote_data.get("municipal_formation")

        # if not all(
        #     elem in request.user.department.locality.all() for elem in vote_localities
        # ):
        #     return Response(
        #         "Некорректное муниципальное образование",
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        questions_data = vote_data.pop("regional_questions", None)
        
        vote = serializer.save()

        questions = []

        for question_data in questions_data:
            answers_data = question_data.pop("regional_answers", None)

            question_id = question_data.get("id", None)
            question_serializer = (
                RegionalVoteUpdateQuestionSerializer(
                    instance=VoteRegionalQuestion.objects.get(pk=question_id),
                    data=question_data,
                )
                if question_id
                else RegionalVoteCreateQuestionSerializer(data=question_data)
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
                    RegionalVoteUpdateAnswerSerializer(
                        instance=VoteRegionalAnswer.objects.get(pk=answer_id),
                        data=answer_data,
                    )
                    if answer_id
                    else RegionalVoteCreateAnswerSerializer(data=answer_data)
                )

                answer_serializer.is_valid(raise_exception=True)
                answer = answer_serializer.save(vote_question=question)
                answers.append(answer)

            if question.max_answer_option_count > len(answers):
                raise ValidationError(
                    "Максимальное количество вариантов ответов больше чем вариантов ответов."
                )

            question.regional_answers.exclude(id__in=[m.pk for m in answers]).delete()
            question.regional_answers.set(answers)
        
        vote.regional_questions.exclude(id__in=[m.pk for m in questions]).delete()
        vote.regional_questions.set(questions)

        return Response(
            RegionalVoteUpdateSerializer(vote).data, status=status.HTTP_200_OK
        )


    @transaction.atomic
    @action(methods=["get"], detail=True)
    def to_moderation(self, request, pk):
        instance: VoteRegional = self.get_object()

        if instance.state != VoteState.DRAFT:
            return Response(
                'Голосование не в статусе "Черновик"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.operator_to_moderation()
        instance.save(update_fields=["state", "to_moderation_date"])

        return Response(
            RegionalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )


    @transaction.atomic
    @action(methods=["get"], detail=True)
    def accept(self, request, pk):
        instance: VoteRegional = self.get_object()

        if instance.state != VoteState.MODERATION_ACCEPTED:
            return Response(
                'Голосование не в статусе "Одобрен модератором"',
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.operator_accept()
        instance.save(update_fields=["state", "operator_action_date"])

        return Response(
            RegionalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def reject(self, request, pk):
        instance: VoteRegional = self.get_object()

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
            RegionalVoteDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )
