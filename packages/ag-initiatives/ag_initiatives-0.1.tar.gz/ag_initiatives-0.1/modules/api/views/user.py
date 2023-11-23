from django.contrib.auth import logout as dj_logout
from rest_framework import permissions, authentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response

from modules.api.serializers import UserShortSerializer


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication])
def user_info(request):
    return Response(UserShortSerializer(request.user).data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.TokenAuthentication])
def logout(request):
    dj_logout(request)
    return Response(data=None, status=200)
