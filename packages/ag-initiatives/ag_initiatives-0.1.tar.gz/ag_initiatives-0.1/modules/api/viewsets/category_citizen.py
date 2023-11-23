from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from django.db import transaction

from modules.api.serializers import UserCategorySerializer, CategoryCitizenSerializer

from modules.core.services import category_citizen_redis
from modules.core.models import CategoryCitizen


class CategoryCitizenAPI(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    model = CategoryCitizen
    queryset = model.objects.all()
    serializer_class = CategoryCitizenSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user:
            raise NotAuthenticated
        response = super().list(request, *args, **kwargs)
        user_categories = UserCategorySerializer(user).data
        response_data = response.data
        for obj in response_data:
            for category_id in user_categories['categories']:
                if category_id == obj['id']:
                    obj.update({"is_user_category": True})
        new_data = {'categories': response_data}
        count_of_changes = category_citizen_redis.get_count_of_changes(user.id)
        if not count_of_changes:
            count_of_changes = 2
        else:
            count_of_changes = 2 - int(count_of_changes)
        restriction_of_changes = {
            "time_left": category_citizen_redis.get_time_left(user.id),
            "count_of_changes_remaining": count_of_changes
        }
        new_data.update(restriction_of_changes)
        return Response(new_data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user:
            raise NotAuthenticated
        user_categories = UserCategorySerializer(data=request.data)
        user_categories.is_valid(raise_exception=True)
        validated_data = user_categories.validated_data
        redis_value = category_citizen_redis.set_restriction_of_changes(user.id)
        if "Changes are no longer available" in redis_value.keys():
            raise PermissionDenied(
                detail=f'Changes are no longer available, time left - {redis_value["Changes are no longer available"]}',
                code=status.HTTP_400_BAD_REQUEST
            )
        user_categories.update(user, validated_data)
        return Response(data=redis_value, status=status.HTTP_200_OK)
