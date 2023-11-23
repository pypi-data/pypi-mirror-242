from requests import Request, Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.serializers import VideoDetailReadSerializer
from modules.core.services.video import VideoService


class VideoApi(viewsets.ViewSet):
    def retrieve(self, request: Request, pk: int):
        instance = VideoService.get_by_id(pk)
        return Response(VideoDetailReadSerializer(instance).data)

    def create(self, request: Request):
        serializer = VideoDetailReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(VideoDetailReadSerializer(instance).data)

    @action(methods=["get"], detail=True)
    def stream(self, request: Request, pk: int):
        return VideoService.get_stream_response(pk=pk, request=request)
