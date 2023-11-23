from rest_framework.decorators import api_view
from rest_framework.response import Response

from modules.core.models import LocalityTypeEnum


@api_view(["GET"])
def localities_categories(request):
    data = {
        "municipalities": {
            k: v for k, v in LocalityTypeEnum.RESOLVER.items() if k in LocalityTypeEnum.MUNICIPALITY_TYPES
        },
        "localities": {
            k: v for k, v in LocalityTypeEnum.RESOLVER.items() if k in LocalityTypeEnum.LOCALITY_TYPES
        },
    }
    return Response(data)
