from requests import Request, Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.serializers import AudioSerializer
from modules.core.services import AudioService


class AudioApi(viewsets.ViewSet):
    def retrieve(self, request: Request, pk: int):
        instance = AudioService.get_by_id(pk)
        return Response(AudioSerializer(instance).data)

    def create(self, request: Request):
        serializer = AudioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(AudioSerializer(instance).data)

    @action(methods=["get"], detail=True)
    def stream(self, request: Request, pk: int):
        return AudioService.get_stream_response(pk=pk, request=request)
