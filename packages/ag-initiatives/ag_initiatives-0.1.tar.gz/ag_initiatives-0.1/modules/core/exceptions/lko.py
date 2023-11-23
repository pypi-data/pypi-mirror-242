from rest_framework.exceptions import APIException


class LkoPermissionError(APIException):
    status_code = 403
    default_detail = "У вас нет прав для выполнения этой операции"
