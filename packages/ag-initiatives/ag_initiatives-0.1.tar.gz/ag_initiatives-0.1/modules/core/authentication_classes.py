from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from modules.integration.models.external_system import ExternalSystemToken


class ExternalSystemTokenAuthentication(BaseAuthentication):
    keyword = "Token"
    model = ExternalSystemToken

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token

        return Token

    """
    A custom token model may be used, but must have the following properties.

    * key -- The string identifying the token
    * user -- The user to which the token belongs
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            msg = "Ошибка авторизации. Токен не указан."
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = "Недопустимый заголовок токена. Не предоставлены учетные данные."
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = "Недопустимый заголовок токена. Токен не должен содержать пробелов."
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = "Недопустимый заголовок токена. Токен не должен содержать недопустимые символы."
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Недопустимый токен.")

        return (token, key)

    def authenticate_header(self, request):
        return self.keyword


HTTP_HEADER_ENCODING = "iso-8859-1"


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth
