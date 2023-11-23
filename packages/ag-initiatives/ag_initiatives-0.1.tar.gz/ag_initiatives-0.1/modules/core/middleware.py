from django.utils.deprecation import MiddlewareMixin

from modules.integration.models.external_system import ExternalSystemToken


class ExternalSystemMiddleware(MiddlewareMixin):
    """
    Middleware for check in request meta fields and set params for organization.

    Check Meta tag "Authorization" for token, which belongs to organization.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token: str = request.META.get("HTTP_AUTHORIZATION")

        if token and token.startswith("Token"):
            request.external_system = self.get_external_system(
                token.replace("Token", "").strip()
            )
        else:
            request.external_system = None

        response = self.get_response(request)
        return response

    def get_external_system(self, token: str):
        try:
            external_system = ExternalSystemToken.objects.prefetch_related("permission").get(key=token)
        except ExternalSystemToken.DoesNotExist:
            external_system = None

        return external_system
