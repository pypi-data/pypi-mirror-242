from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from modules.core.authentication_classes import ExternalSystemTokenAuthentication
from modules.core.models.user import User
from modules.ecology.api.serializers.user_purchase import UserPurchaseSerializer
from modules.ecology.models.event import Event
from modules.ecology.models.goods_n_services_item import GoodsNServicesItem
from modules.integration.models.user_synchronization import UserSynchronization
from modules.integration.permissions import CanUseEncouragements, CanUseSuggestions


from modules.ecology.exceptions import BalanceOperationError, UserError
from modules.ecology.services import QRGenerator
from modules.ecology.services.user_service import UserService


from django.http import HttpResponse


class ExternalSystemGoodNServicesApi(APIView):
    permission_classes = [CanUseEncouragements]
    authentication_classes = [ExternalSystemTokenAuthentication]

    def post(self, request):
        user: User = User.objects.filter(pk=request.data.get("user_id")).first()
        synchronized_user = UserSynchronization.objects.filter(user_id=user.pk).exists()

        if not user or not synchronized_user:
            return Response(
                "Неверно указан идентификатор пользователя или он не синхронизирован.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        item_id = request.data.get("reward_id")
        item: GoodsNServicesItem = GoodsNServicesItem.objects.filter(pk=item_id).first()
        if not item:
            return Response("Данного поощрения не существует")

        try:
            purchase = UserService(user).purchase(item)
        except (UserError, BalanceOperationError) as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserPurchaseSerializer(purchase).data)


class ExternalSystemEventApi(APIView):
    permission_classes = [CanUseSuggestions]
    authentication_classes = [ExternalSystemTokenAuthentication]

    def post(self, request):
        user: User = User.objects.filter(id=request.data.get("user_id")).first()
        synchronized_user = UserSynchronization.objects.filter(user_id=user.pk).exists()

        if not user or not synchronized_user:
            return Response(
                "Неверно указан идентификатор пользователя или он не синхронизирован.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        event_id = request.data.get("offer_id", None)
        if not event_id:
            return Response(
                "Не указан id предложения", status=status.HTTP_400_BAD_REQUEST
            )

        event: Event = Event.objects.filter(pk=event_id).first()
        if not event:
            return Response(
                "Предложение не найдено", status=status.HTTP_400_BAD_REQUEST
            )

        try:
            participation_user_event = UserService(user).event_participate(event)
        except UserError as err:
            return Response(err.message, status=status.HTTP_400_BAD_REQUEST)

        host = QRGenerator.get_host(request)
        qr_data = f"{host}organizer/qr-scan/{participation_user_event.pk}"
        svg_qrcode = QRGenerator(qr_data).svg
        return HttpResponse(svg_qrcode, content_type="image/svg+xml")
