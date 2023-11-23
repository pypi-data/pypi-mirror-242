from rest_framework.response import Response
from rest_framework.views import APIView

from modules.core.authentication_classes import ExternalSystemTokenAuthentication


class CheckSystemAccessApi(APIView):
    """API for check access to system for specific token, which hand out for external systems."""

    authentication_classes = (ExternalSystemTokenAuthentication,)

    def get(self, request):
        """Return success status code, if authentication was passed."""
        return Response("Система доступна для использования", status=200)
