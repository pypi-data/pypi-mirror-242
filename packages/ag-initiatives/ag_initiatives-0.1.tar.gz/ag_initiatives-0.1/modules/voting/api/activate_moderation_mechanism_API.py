from rest_framework.views import APIView
from rest_framework.response import Response

from modules.voting.api.serializers import ActivationModerationMechanismSerializer
from modules.voting.models import ActivationModerationMechanism


class ActivateModerationMechanismAPI(APIView):
    def get(self, request):
        qs = ActivationModerationMechanism.objects.last()
        return Response({"state": ActivationModerationMechanismSerializer(qs).data})