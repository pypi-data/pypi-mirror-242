from collections import OrderedDict

from django.db import transaction
from django.db.models import Prefetch, Exists, OuterRef, Q, Subquery, BooleanField, Case, When, Value
from pydantic import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from modules.api.pagination import DefaultPagination
from modules.api.serializers import CategoryCitizenSerializer
from modules.api.viewsets.filters.voting import VotingFilter
from modules.api.viewsets.operator_lko.serializers.locality import (
    MunicipalityWithUnavailableTreeSerializer
)
from modules.api.viewsets.operator_lko.serializers.voting import VoteOperatorLkoListSerializer
from modules.core.models import User, CategoryCitizen
from modules.core.models.permissions import ModulesPermissions
from modules.core.permissions import IsOperator
from modules.core.services.operator_lko import OperatorLkoService
from modules.voting.api.serializers import (
    VoteOperatorCreateSerializer,
    VoteOperatorDetailsSerializer,
    CategoryDetailsSerializer,
    LocalityDetailsSerializer, VoteOperatorUpdateQuestionSerializer, VoteOperatorUpdateSerializer,
    VoteOperatorUpdateAnswerOptionSerializer, VoteOperatorCreateAnswerOptionSerializer,
)
from modules.voting.api.serializers.vote_operator import VoteOperatorCreateQuestionSerializer
from modules.voting.mixins.vote_admin_mixin import vote_report2
from modules.voting.models import VoteState, Vote, VoteQuestion, VoteAnswerOption
from modules.voting.services.mail_service import MailService


class VotingOperatorLkoAPI(viewsets.ReadOnlyModelViewSet):
    """API для голосований Оператора ЛКО"""
    queryset = Vote.objects.none()
    permission_classes = [IsOperator]
    service_class = OperatorLkoService
    filterset_class = VotingFilter
    serializer_class = VoteOperatorLkoListSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return (Vote.objects.filter(
            locality__in=self.request.user.sub_permissions.operator_permissions.voting_localities.all().values_list(
                'id', flat=True),
            department__in=[self.request.user.sub_permissions.operator_permissions.department.id],
            category__in=self.request.user.sub_permissions.operator_permissions.voting_categories.all().values_list(
                'id', flat=True),
        ).distinct()
         .order_by("-creation_date")
         .prefetch_related(
            Prefetch("questions", queryset=VoteQuestion.objects.order_by("order")),
            Prefetch(
                "questions__answers",
                queryset=VoteAnswerOption.objects.order_by("order"),
            ),
            )
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
        service = self.service_class(user=user, module=ModulesPermissions.VOTING)

        data = {
            "status": dict(VoteState.CHOICES),
            "localities": LocalityDetailsSerializer(user.sub_permissions.operator_permissions.voting_localities.all(),
                                                    many=True).data,
            "categories": CategoryDetailsSerializer(user.sub_permissions.operator_permissions.voting_categories.all(),
                                                    many=True).data,
            "participants_categories": CategoryCitizenSerializer(CategoryCitizen.objects.all(), many=True).data
        }
        return Response(data)

    @action(methods=["get"], detail=False)
    def info_info(self, request, *args, **kwargs):
        # operator = OperatorLkoService(
        #     user=self.request.user,
        #     module=ModulesPermissions.VOTING
        # )
        # data = {
        #     'localities': get_divided_municipalities_data(
        #         get_municipalities_with_unavailable_from_localities(
        #             operator.get_allowed_localities()
        #         )
        #     )
        # }
        data = {
            'localities': {
                "municipal_regions": [],
                "municipal_districts": [],
                "urban_districts": MunicipalityWithUnavailableTreeSerializer(
                    self.request.user.sub_permissions.operator_permissions.voting_localities.all().order_by("order",
                                                                                                            "name"),
                    many=True).data
            }
        }
        return Response(data)

    @action(methods=["get"], detail=True)
    def xls(self, request, pk):
        qs = self.filter_queryset(self.get_queryset())
        return vote_report2(None, request, qs.filter(pk=pk))

    @action(methods=["get"], detail=False, url_path='xls-zip')
    def xls_zip(self, request):
        qs = self.filter_queryset(self.get_queryset())
        return vote_report2(None, request, qs)

    @transaction.atomic
    @action(methods=["post"], detail=False)
    def add(self, request):
        user: User = request.user
        serializer = VoteOperatorCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        vote_data = serializer.validated_data

        vote_localities = vote_data.pop("locality")

        service = self.service_class(user=user, module=ModulesPermissions.VOTING)

        if not all(
                elem in user.sub_permissions.operator_permissions.voting_localities.all() for elem in vote_localities
        ):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions = vote_data.pop("questions", None)

        vote = Vote.objects.create(
            **vote_data,
            state=VoteState.DRAFT,
            department=user.sub_permissions.operator_permissions.department,
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
    @action(methods=["get"], detail=True)
    def copy(self, request, pk):
        instance: Vote = self.get_object()
        localities = instance.locality.all()
        questions = instance.questions.all()

        instance.pk = None
        instance.state = VoteState.DRAFT
        instance.moderation_date = None
        instance.operator_action_date = None
        instance.save()

        for locality in localities:
            instance.locality.add(locality)

        for question in questions:
            answers = question.answers.all()
            question.pk = None
            question.save()
            for answer in answers:
                answer.pk = None
                answer.save()
                question.answers.add(answer)
            instance.questions.add(question)

        MailService.notify_moderator__vote_created(vote=instance)

        return Response(
            VoteOperatorDetailsSerializer(instance).data, status=status.HTTP_201_CREATED
        )

    @transaction.atomic
    @action(methods=["get", "put"], detail=True, url_path="update-details")
    def update_details(self, request, pk):
        vote: Vote = self.get_object()

        user: User = request.user

        service = self.service_class(user=user, module=ModulesPermissions.VOTING)

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

        if not all(
                elem in user.sub_permissions.operator_permissions.voting_localities.all() for elem in vote_localities
        ):
            return Response(
                "Некорректное муниципальное образование",
                status=status.HTTP_400_BAD_REQUEST,
            )

        questions_data = vote_data.pop("questions", None)

        vote = serializer.save()

        questions: list = []
        for question_data in questions_data:
            answers_data = question_data.pop("answers", None)

            question_id = question_data.get("id", None)
            question_data = OrderedDict((key, value.id if key in ['photo', 'video', 'file'] and value else value)
                                        for key, value in question_data.items())

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

                answer_image = answer_data.pop("image", None)
                answer_data["image"] = answer_image.pk if answer_image else None

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

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})
