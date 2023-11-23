from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action


from modules.core.models import User
from modules.core.permissions import IsOperator
from modules.ecology.api.serializers.user_balance_operation import (
    PartnerHistorySerializer,
    PartnerHistoryExcelSerializer,
)
from modules.ecology.api.serializers.user_purchase import PartnerPurchaseSerializer
from modules.ecology.exceptions import PartnerError
from modules.ecology.models import UserPurchase
from modules.ecology.pagination import DefaultPagination

from modules.ecology.services.partner_service import PartnerService
from modules.ecology.services.search import get_search_filter_by_user_fio


class PartnerAPI(viewsets.ViewSet):
    permission_classes = [IsOperator]

    @action(methods=["get"], detail=False)
    def counts(self, request):
        partner: User = request.user

        try:
            partner_service = PartnerService(partner)
            history_count = partner_service.get_history().count()
            purchases_count = partner_service.get_users_purchases().count()
        except PartnerError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        return Response({"rewards_receive": purchases_count, "history": history_count})


class PartnerHistoryAPI(viewsets.ViewSet):
    permission_classes = [IsOperator]

    def list(self, request):
        partner: User = request.user

        try:
            queryset = PartnerService(partner).get_history()
        except PartnerError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        paginator = DefaultPagination()
        page = paginator.paginate_queryset(queryset, request=request)
        response = paginator.get_paginated_response(
            PartnerHistorySerializer(page, many=True).data
        )
        return response

    @action(methods=["get"], detail=False)
    def excel(self, request):
        partner: User = request.user

        try:
            queryset = PartnerService(partner).get_history()
        except PartnerError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        json_data = PartnerHistoryExcelSerializer(queryset, many=True).data

        return PartnerHistoryExcelSerializer.excel_response(
            json_data, response_status=200
        )


class PartnerPurchaseAPI(viewsets.ViewSet):
    permission_classes = [IsOperator]

    def list(self, request):
        partner: User = request.user

        try:
            queryset = PartnerService(partner).get_users_purchases()
        except PartnerError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        search = request.query_params.get("search", None)

        if search:
            queryset = queryset.filter(get_search_filter_by_user_fio(search))

        paginator = DefaultPagination(page_size=3)
        page = paginator.paginate_queryset(queryset, request=request)
        response = paginator.get_paginated_response(
            PartnerPurchaseSerializer(page, many=True).data
        )
        return response

    def partial_update(self, request, pk):
        partner: User = request.user
        code: str = request.data.get("code", None)
        purchase: UserPurchase = UserPurchase.objects.filter(pk=pk).first()

        if not purchase:
            return Response(
                "Запрос на получение поощрения не найден",
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not code:
            return Response(
                "Не предоставлен код подтверждения", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            purchase = PartnerService(partner).confirm_purchase(
                purchase=purchase, code=code
            )
        except PartnerError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(PartnerPurchaseSerializer(purchase).data)
