from typing import Optional

import requests
from pydantic import BaseModel
from requests import Response

from config.settings import settings


class SmevAdapterPaths:
    SEND_REQUEST = "/api/smev/1-2/send-request"
    DOWNLOAD_FILE = "/api/smev/1-2/get-file"
    UPLOAD_FILES = "/api/smev/1-2/upload-files"
    ACK_REQUEST = "/api/smev/1-2/ack-request"


class FileSaveResponse(BaseModel):
    FileId: str


class PosSmevHttpClient:
    """
    Класс, который отправляет запросы на ПОС сервер и возвращает их в формате Response объекта
    """
    REGION_ID = settings.REGION_ID
    smev_url = 'http://smev-adapter:8000'
    paths = SmevAdapterPaths

    def smev_send_request(self, data: bytes) -> Response:
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(
            f"{self.smev_url}{self.paths.SEND_REQUEST}",
            data=data,
            headers=headers,
            verify=False
        )
        return response

    def send_file(self, files) -> Response:
        response = requests.post(
            f"{self.smev_url}{self.paths.UPLOAD_FILES}",
            files=files,
            verify=False,
        )

        return response

    def send_files_to_pos(self, appeal_data: str, files_ids: list) -> Response:
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(
            f"{self.smev_url}{self.paths.SEND_REQUEST}",
            data=appeal_data,
            params={"files_ids": files_ids},
            headers=headers,
            verify=False
        )
        return response

    def get_response_from_queue(self):
        headers = {'Content-Type': 'application/xml'}
        response = requests.get(
            f"{self.smev_url}{self.paths.SEND_REQUEST}",
            headers=headers,
            verify=False,
        )
        return response

    def ack_request(self, message_id):
        response = requests.post(
            f"{self.smev_url}{self.paths.ACK_REQUEST}",
            json={"message_id": str(message_id)},
            verify=False,
        )
        return response

    def download_file(self, file_id: str, username: str, password: str) -> Optional[bytes]:
        response = requests.post(
            f"{self.smev_url}{self.paths.DOWNLOAD_FILE}",
            json={
                "file_id": file_id,
                "username": username,
                "password": password,
            },
            verify=False,
        )
        if 200 <= response.status_code < 300:
            return response.content
        return None
