from requests import Response

from config.settings import settings
from modules.appeals_pos.services import PosSession


class PosPaths:
    REGIONS_LIST = "/inbox-service/regions/all"
    SUBJECTS_LIST = "/inbox-service/subjects/region/{}/all"
    SUBJECTS_LIST_FULL = "/inbox-service/subjects/region/{}"
    SUBSUBJECTS_LIST_BY_SUBJECT = "/inbox-service/subsubjects/subject/{}/region/{}"
    SUBSUBJECTS_LIST_SEARCH = "/inbox-service/subsubjects/search"
    FILE_ADD = "/inbox-service/filestorage"

    APPEAL_ADD = "/inbox-service/external-appeal-system/appeals"
    APPEL_GET_STATUS = "/appeal-service/external-appeal-system/appeals/{}"


class PosHttpClient:
    """
    Класс, который отправляет запросы на ПОС сервер и возвращает их в формате Response объекта
    """
    REGION_ID = settings.REGION_ID
    session = PosSession()
    paths = PosPaths

    def get_regions_list(self) -> Response:
        response = self.session.configure_request(
            method="get", path=self.paths.REGIONS_LIST
        ).make_request()
        return response

    def get_subjects_list(self) -> Response:
        response = self.session.configure_request(
            method="get", path=self.paths.SUBJECTS_LIST.format(self.REGION_ID)
        ).make_request()
        return response

    def get_subjects_list_full(self, size=10000) -> Response:
        response = self.session.configure_request(
            method="get",
            path=self.paths.SUBJECTS_LIST_FULL.format(self.REGION_ID),
            params={"size": size},
        ).make_request()
        return response

    def get_subsubjects_list_by_subject(self, subject_id) -> Response:
        response = self.session.configure_request(
            method="get",
            path=self.paths.SUBSUBJECTS_LIST_BY_SUBJECT.format(
                subject_id, self.REGION_ID
            ),
        ).make_request()
        return response

    def get_subsubjects_list(self, size=10000) -> Response:
        response = self.session.configure_request(
            method="get",
            path=self.paths.SUBSUBJECTS_LIST_SEARCH,
            params={"regionId": self.REGION_ID, "size": size},
        ).make_request()
        return response

    def get_appeal_data(self, appeal_id) -> Response:
        response = self.session.configure_request(
            method="get", path=self.paths.APPEL_GET_STATUS.format(appeal_id)
        ).make_request()
        return response

    def add_appeal(self, appeal_data: dict) -> Response:
        response = self.session.configure_request(
            method="post",
            path=self.paths.APPEAL_ADD,
            data=appeal_data,
            headers={"Content-Type": "application/json"},
        ).make_request()
        return response

    def send_file(self, file) -> Response:
        response = self.session.configure_request(
            method="post", path=self.paths.FILE_ADD, data={"file": file}
        ).make_file_request()

        return response
