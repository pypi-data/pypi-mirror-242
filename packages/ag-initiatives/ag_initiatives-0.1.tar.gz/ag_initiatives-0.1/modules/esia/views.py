import json

from django.contrib.auth import authenticate, login
from django.core.cache import caches
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes


@csrf_exempt
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    esia_data = json.loads(request.body)
    user = authenticate(esia_data=esia_data, create_user=True)
    if user is None:
        raise Http404("No such user registered")
    esia_data_cache = caches["esia_raw_data"]
    esia_data_cache.set(user.pk, esia_data)
    auth_token, created = Token.objects.get_or_create(user=user)

    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])

    return JsonResponse(
        status=200,
        data={
            "redirect_params": "",
            "auth_token": auth_token.key,
        },
    )
