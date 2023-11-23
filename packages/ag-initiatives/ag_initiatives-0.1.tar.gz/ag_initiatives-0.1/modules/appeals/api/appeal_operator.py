import time

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status

from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from modules.appeals.api.filters import AppealFilter
from modules.appeals.api.serializers import (
    AppealOperatorListSerializer,
    AppealOperatorDetailsSerializer,
    ContractorSerializer,
    AppealInProgressOperatorSerializer,
    AppealResponseShortSerializer,
    AppealResponseCreateSerializer,
    CategoryDetailedSerializer,
    AppealStateChangeShortSerializer,
    AppealOperatorCreateSerializer,
    CategoryTreeSerializer,
    AppealOwnerCommunicationsOperatorSerializer,
)
from modules.appeals.models import (
    Appeal,
    AppealState,
    Contractor,
    AppealResponse,
    File,
    DepartmentCategory,
    AppealStateChange,
    Category,
)
from modules.appeals.services.mail_service import MailService
from modules.core.models import User
from modules.core.permissions import IsOperator


class AppealOperatorAPI(viewsets.ReadOnlyModelViewSet):
    queryset = Appeal.objects.none()
    serializer_class = AppealOperatorListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AppealFilter
    permission_classes = [IsOperator]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        categories = [
            e.category
            for e in DepartmentCategory.objects.filter(
                department=self.request.user.department
            )
        ]
        return (
            Appeal.objects.filter(
                state__in=[
                    AppealState.MODERATION_ACCEPTED,
                    AppealState.IN_PROGRESS,
                    AppealState.RESPONDED,
                ],
                category__in=categories,
            )
            .order_by("-moderation_pass_date")
            .select_related(
                "locality",
                "category",
                "category__parent",
            )
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AppealOperatorDetailsSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def count(self, request):
        return Response({"count": self.filter_queryset(self.get_queryset()).count()})

    # @action(methods=['get'], detail=False)
    # def categories(self, request):
    #     data = CategoryDetailedSerializer(
    #         [e.category for e in DepartmentCategory.objects.filter(department=request.user.department)],
    #         many=True
    #     ).data
    #     return Response(data)

    @action(methods=["get"], detail=False)
    def categories(self, request):
        return Response(
            CategoryTreeSerializer(
                Category.objects.filter(parent__isnull=True), many=True
            ).data
        )

    @action(methods=["get"], detail=False)
    def contractors(self, request):
        return Response(ContractorSerializer(Contractor.objects.all(), many=True).data)

    @action(methods=["get"], detail=True, url_path="contractors")
    def item_contractors(self, request, pk):
        instance: Appeal = self.get_object()
        return Response(ContractorSerializer(instance.contractors, many=True).data)

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def in_progress(self, request, pk):
        instance: Appeal = self.get_object()

        if instance.state != AppealState.MODERATION_ACCEPTED:
            return Response(
                "Обращение не на рассмотрении", status=status.HTTP_400_BAD_REQUEST
            )

        if DepartmentCategory.objects.filter(category=instance.category).count() == 0:
            return Response(
                "На категорию обращения не назначено ведомства",
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AppealInProgressOperatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contractors = Contractor.objects.filter(
            pk__in=serializer.validated_data["contractors"]
        )

        instance.contractors.add(*contractors)
        instance.operator_in_progress()
        instance.save(update_fields=["state", "in_progress_begin_date"])

        AppealStateChange.objects.create(
            appeal=instance,
            new_state=instance.state,
            user=request.user,
            department=request.user.department,
        )

        MailService.notify_user_in_progress(instance)
        MailService.notify_contractors_in_progress(instance)

        return Response(
            AppealOperatorDetailsSerializer(instance).data, status=status.HTTP_200_OK
        )

    @transaction.atomic
    @action(methods=["post"], detail=True)
    def respond(self, request, pk):
        instance: Appeal = self.get_object()

        if instance.state != AppealState.IN_PROGRESS:
            return Response("Обращение не в работе", status=status.HTTP_400_BAD_REQUEST)

        if AppealResponse.objects.filter(appeal=instance).exists():
            return Response(
                "На обращение ответ уже дан", status=status.HTTP_400_BAD_REQUEST
            )

        if request.user.department is None:
            return Response(
                "Пользователь без ведомства", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AppealResponseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        files = File.objects.filter(pk__in=serializer.validated_data.pop("files", []))
        response = AppealResponse.objects.create(
            appeal=instance,
            user=request.user,
            department=request.user.department,
            timestamp=timezone.now(),
            **serializer.validated_data,
        )
        response.files.add(*files)
        response.save()

        instance.operator_respond()
        instance.save(update_fields=["state", "responded_date"])

        AppealStateChange.objects.create(
            appeal=instance,
            new_state=instance.state,
            user=request.user,
            department=request.user.department,
        )

        MailService.notify_user_responded(instance)

        return Response(status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True, url_path="notifications")
    def item_notifications(self, request, pk):
        instance: Appeal = self.get_object()
        queryset = AppealStateChange.objects.filter(appeal=instance).order_by(
            "-timestamp"
        )
        return Response(AppealStateChangeShortSerializer(queryset, many=True).data)

    @transaction.atomic
    @action(methods=["post"], detail=False)
    def add(self, request):
        serializer = AppealOperatorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appeal_data = serializer.validated_data
        files = appeal_data.pop("files", None)

        applicant_first_name = appeal_data.pop("applicant_first_name")
        applicant_patronymic_name = appeal_data.pop("applicant_patronymic_name")
        applicant_last_name = appeal_data.pop("applicant_last_name")
        applicant_phone_number = appeal_data.get("phone_number")

        category = appeal_data.get("category")

        operator_categories = [
            e.category
            for e in DepartmentCategory.objects.filter(
                department=self.request.user.department
            )
        ]

        if category not in operator_categories:
            return Response(
                "Выбрана некорректная категория", status=status.HTTP_400_BAD_REQUEST
            )

        applicant: User = None
        try:
            applicant = User.objects.get(
                first_name=applicant_first_name,
                last_name=applicant_last_name,
                patronymic_name=applicant_patronymic_name,
            )
        except User.DoesNotExist:
            applicant = User(
                username=f"generated_{int(time.time())}",
                first_name=applicant_first_name,
                last_name=applicant_last_name,
                patronymic_name=applicant_patronymic_name,
                phone=applicant_phone_number,
                email="",
                is_active=False,
            )
            applicant.save()

        appeal = Appeal.objects.create(
            number="",
            user=applicant,
            state=AppealState.MODERATION_ACCEPTED,
            create_by_operator=True,
            **appeal_data,
        )

        if files is not None:
            appeal.files.set(files)
        appeal.number = f"О-{appeal.pk:0>10d}"
        appeal.save(update_fields=["number"])

        # AppealStateChange.objects.create(
        #     appeal=appeal,
        #     new_state=appeal.state
        # )

        return Response(
            AppealOperatorDetailsSerializer(appeal).data, status=status.HTTP_201_CREATED
        )

    @action(methods=["get"], detail=True, url_path="owner-communications")
    def owner_communications(self, request, pk):
        instance: Appeal = self.get_object()
        return Response(
            AppealOwnerCommunicationsOperatorSerializer(
                instance.owner_communications.all().order_by("-timestamp"), many=True
            ).data
        )
