from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from modules.api.serializers import ActiveCitizenModuleSerializer, ProjectInfoSerializer
from modules.core.models import ActiveCitizenModule, ProjectInfo


class ActiveCitizenModuleViewset(viewsets.ModelViewSet):
    queryset = ActiveCitizenModule.objects.all().order_by('-id')
    serializer_class = ActiveCitizenModuleSerializer
    http_method_names = ["get", "patch"]

    @action(detail=True, methods=["patch"])
    def switch(self, request, pk):
        module = self.queryset.filter(pk=pk).first()
        module.switch()
        data = self.serializer_class(module).data
        return Response(data, status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["get"])
    def enabled(self, request, *args, **kwargs):
        modules = self.queryset.filter(is_worked=True).values('id', 'name', 'display_name')
        return Response(modules, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        qs = ProjectInfo.objects.filter(site_module=kwargs['pk'], site_module__is_worked=True)
        serializer = ProjectInfoSerializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
