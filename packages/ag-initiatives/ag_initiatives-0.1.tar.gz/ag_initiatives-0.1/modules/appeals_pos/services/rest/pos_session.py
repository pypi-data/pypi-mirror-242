import base64
import logging
from typing import Optional

import requests
from requests import Response, Session, HTTPError
from rest_framework import status
from rest_framework.exceptions import ValidationError

from config.settings import settings
from modules.appeals_pos.services.rest.pos_structs import (
    AuthDataStruct,
    AuthResponseStruct,
)

logger = logging.getLogger(name="appeals.request")


class PosSettings:
    BODY_USERNAME = settings.POS_CLIENT_ID
    BODY_PASSWORD = settings.POS_BODY_PASSWORD
    BASIC_AUTH_USERNAME = settings.POS_BASIC_AUTH_USERNAME
    BASIC_AUTH_PASSWORD = settings.POS_BASIC_AUTH_PASSWORD
    DEBUG = settings.POS_DEBUG
    SCOPE = "any"
    GRANT_TYPE = "password"

    @property
    def basic_auth_key(self) -> str:
        return base64.b64encode(
            f"{self.BASIC_AUTH_USERNAME}:{self.BASIC_AUTH_PASSWORD}".encode()
        ).decode()


class PosSession:

    """Класс для конфигурирования запросов на ПОС, сам проходит авторизацию если требуется и т.п."""

    pos_settings = PosSettings()

    def __init__(self, headers: dict = None):
        self.method: Optional[str] = None
        self.path: Optional[str] = None
        self.data: Optional[dict] = None
        self.params: Optional[str] = None

        self.domain = self._get_domain()
        self.session = Session()
        if headers:
            self.add_headers(headers)

    def _get_domain(self) -> str:
        if self.pos_settings.DEBUG:
            return "pos2.test.gosuslugi.ru"
        return "pos.gosuslugi.ru"

    def _get_url(self) -> str:
        return f"https://{self.domain}{self.path}"

    def add_headers(self, headers: dict):
        self.session.headers.update(headers)
        return self

    def add_header(self, key: str, value: str):
        self.session.headers[key] = value
        return self

    def _make_auth_request(self) -> AuthResponseStruct:
        data = AuthDataStruct(
            username=self.pos_settings.BODY_USERNAME,
            password=self.pos_settings.BODY_PASSWORD,
            scope=self.pos_settings.SCOPE,
            grant_type=self.pos_settings.GRANT_TYPE,
        )
        response = requests.post(
            f"https://{self.domain}/user-service/oauth/token",
            data=data.to_dict(),
            headers={"Authorization": f"Basic {self.pos_settings.basic_auth_key}"},
            verify=False,
        )
        try:
            response.raise_for_status()
        except HTTPError as err:
            raise ValidationError(err.response.text)
        return AuthResponseStruct(**response.json())

    @property
    def url(self):
        return self._get_url()

    @property
    def headers(self):
        return self.session.headers

    def set_empty_auth_header(self):
        self.add_header("Authorization", "Bearer ")

    def auth(self):
        token = self._make_auth_request().access_token
        self.add_header("Authorization", f"Bearer {token}")

    def configure_request(
        self,
        method: str,
        path: str,
        params: dict = None,
        data: dict = None,
        headers: dict = None,
    ):
        self.method = method
        self.path = path
        self.params = params if params else None
        self.data = data if data else None
        if headers:
            self.add_headers(headers)
        return self

    def make_file_request(self):
        response = self.session.request(
            method=self.method,
            url=self.url,
            params=self.params,
            files=self.data,
            headers=self.headers,
        )

        if response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]:
            self.auth()
            response = self.session.request(
                method=self.method,
                url=self.url,
                params=self.params,
                files=self.data,
                headers=self.headers,
            )
        log_data = {
            "request": {
                "method": self.method,
                "url": self.url,
                "data": self.data,
            },
            "response": {"status": response.status_code},
        }
        try:
            response.raise_for_status()
            logger.info(log_data)
        except HTTPError:
            logger.error(log_data)
            raise ValidationError(response.content)
        return response

    def make_request(self) -> Response:
        self.headers.pop("Content-Type", None)
        response = self.session.request(
            method=self.method,
            url=self.url,
            params=self.params,
            json=self.data,
            headers=self.headers,
        )
        if response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]:
            self.auth()
            response = self.session.request(
                method=self.method,
                url=self.url,
                params=self.params,
                json=self.data,
                headers=self.headers,
            )
        log_data = {
            "request": {
                "method": self.method,
                "url": self.url,
                "data": self.data,
            },
            "response": {"status": response.status_code},
        }
        try:
            response.raise_for_status()
            logger.info(log_data)
        except HTTPError:
            logger.error(log_data)
            raise ValidationError(response.content)
        return response
