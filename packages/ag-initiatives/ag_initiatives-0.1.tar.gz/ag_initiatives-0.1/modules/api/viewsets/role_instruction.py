from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from modules.api.serializers import RoleInstructionSerializer
from modules.api.filters import RoleInstructionsFilter
from modules.core.models import RoleInstruction


class RoleInstructionViewSet(viewsets.ViewSet):
    queryset = RoleInstruction.objects.all()
    serializer_class = RoleInstructionSerializer
    filter_class = RoleInstructionsFilter

    def list(self, request):
        filtered_queryset = self.filter_class(
            data=request.query_params, queryset=self.queryset
        ).qs
        serializer = RoleInstructionSerializer(filtered_queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        role_instructions = RoleInstruction.objects.filter(id=pk).first()
        if not role_instructions:
            raise NotFound()
        serializer = self.serializer_class(role_instructions)
        return Response(serializer.data)
