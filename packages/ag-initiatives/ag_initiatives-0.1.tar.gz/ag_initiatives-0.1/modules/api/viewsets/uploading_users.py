from rest_framework import viewsets
from modules.api.viewsets.filters import UserFilter
from modules.core.permissions import IsAdminLKO
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from modules.api.serializers import UploadingUsersSerializer
from modules.core.models.permissions import SubPermissions
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer


class UploadingUsersAPI(XLSXFileMixin, viewsets.ModelViewSet):
    queryset = SubPermissions.objects.order_by('id')
    serializer_class = UploadingUsersSerializer
    # permission_classes = (IsAdminLKO,)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    # filterset_class = UserFilter
    # ordering_fields = ["-id"]
    renderer_classes = (XLSXRenderer,)
    filename = "Users.xlsx"

    column_header = {
        'titles': [
            "id", "sub_permissions", "email", "sub_phone", "position",
        ],
        'column_width': [20, 40, 20], 'height': 40, 'style': {
            'fill': {
                'fill_type': 'solid', 'start_color': 'E6E6FA',
            }, 'alignment': {
                'horizontal': 'center',
                'vertical': 'center', 'wrapText': True, 'shrink_to_fit': True,
            }, 'border_side': {
                'border_style': 'thin', 'color': 'FF000000',
            }, 'font': {
                'name': 'Arial', 'size': 14, 'bold': True,
                'color': 'FF000000',
            },
        },
    }
    body = {'style': {
        'fill': {
            'fill_type': 'solid', 'start_color': 'FFFFFF',
        }, 'alignment': {'horizontal': 'center',
                         'vertical': 'center',
                         'wrapText': True, 'shrink_to_fit': True,
                         }, 'border_side': {
            'border_style': 'thin', 'color': 'FF000000',
        }, 'font': {
            'name': 'Times New Roman', 'size': 14, 'bold': False, 'color': 'FF000000',
        }
    }, 'height': 40,
    }
