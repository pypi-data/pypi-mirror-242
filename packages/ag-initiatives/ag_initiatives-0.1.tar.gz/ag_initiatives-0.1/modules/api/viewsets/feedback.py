from des.models import DynamicEmailConfiguration
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from config import settings
from modules.api.serializers import FeedbackSerializer
from modules.core.models import Feedback
from modules.core.tasks import send_mail_with_with_feedback

import requests


class FeedbackViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Feedback.objects.none()
    serializer_class = FeedbackSerializer

    def create(self, request, *args, **kwargs):

        if settings.RECAPTCHA_ENABLED:
            data = {
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": request.data.get("g-recaptcha-response"),
            }
            result = requests.post(
                "https://www.google.com/recaptcha/api/siteverify", data=data, verify=False
            ).json()
            if not result["success"]:
                return Response(
                    result.get("error-codes", "recaptcha error"),
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        from_email = str(DynamicEmailConfiguration.get_solo().from_email)
        send_mail_with_with_feedback.apply_async(
            args=(
                serializer.validated_data,
                settings.FEEDBACK_RECEIVER_EMAIL,
                from_email,
            )
        )
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
