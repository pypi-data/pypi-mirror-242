from rest_framework import viewsets

from modules.api.serializers import DeletionNotificationSerializer
from modules.core.models import DeletionNotification


class DeletionNotificationAPI(viewsets.ModelViewSet):
    """ API для оповещений об удалении учётной записи. """
    queryset = DeletionNotification.objects.all()
    serializer_class = DeletionNotificationSerializer
