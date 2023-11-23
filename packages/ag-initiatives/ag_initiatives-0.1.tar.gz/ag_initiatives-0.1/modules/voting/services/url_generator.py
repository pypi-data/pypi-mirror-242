from typing import Dict

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.exceptions import ValidationError

from modules.voting.enums import VoteType
from modules.voting.models import LocalVotingGroup, Vote


class URLGenerator:
    """Генератор URL
    Вход:
        * объект LocalVotingGroup.
    Поля:
        * _uuid_ - уникальный идентификатор группы;
        * _vote_ - объект Vote;
        * _path_ - адрес сайта.
    Методы:
        * set_path_from_request - установить адрес сервера из запроса;
        * set_path - установить адрес сервера вручную;
        * get - получить данные для ссылки;
        * _check_vote_ - проверить тип голосования.
    Выход:
        * _check_vote_ формирует исключение ValidationError,
            если голосование не является локальным
        * get() формирует словарь:
        +
        ----
        {
            path: {_path_},
            endpoint: /api/vote/{_vote_.id}/local_vote/,
            token: access_token={_uuid_},
        }
        ----
        +
        где path - адрес сервера,
        endpoint - путь к бэкенд-эндпоинту для передачи ответов по голосованию,
        token - пара `ключ=значение` для добавления в url
    Полный URL для передачи ответов на бэкенде:

    ----
    {адрес_сервера}/{endpoint}/?{token}
    ----

    Пример:

    ----
    http://127.0.0.1:8000/api/vote/1/local_vote/access_token=1d1207af-20ad-4ab6-a5bb-561e0f0f7504
    ----

    """

    def __init__(self, vote: Vote, group: LocalVotingGroup) -> None:
        self._uuid_: str = getattr(group, "access_token")
        self._group_id_: str = getattr(group, "id")
        self._vote_: Vote = vote
        self._path_: str = ""

    def set_path_from_request(self, request: WSGIRequest) -> None:
        protocol = ["http", "https"][request.is_secure()]
        host = request.get_host().split(":")[0]
        port = ""
        if request.get_port() not in ["80", "443"]:
            port = f":{request.get_port()}"
        self._path_ = f"{protocol}://{host}{port}"

    def set_path(self, value: str) -> None:
        self._path_ = value

    def get(self) -> Dict:
        return {
            "group_id": f"{self._group_id_}",
            "path": f"{self._path_}",
            "endpoint": f"/api/vote/{self._vote_.id}/local_vote/",
            "token": f"?access_token={self._uuid_}",
        }
