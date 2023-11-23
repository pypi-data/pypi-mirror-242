import logging
from typing import List, Iterable

from modules.appeals_pos.models.file import File
from modules.appeals_pos.services.rest import pos_structs
from modules.appeals_pos.services.rest.pos_client import PosHttpClient

logger = logging.getLogger("POS service")


class PosService:

    """
    Класс, предоставляющий простой интерфейс для работы с интеграцией ПОС.
    Возвращает удобные для работы структуры данных
    """

    http_client = PosHttpClient()

    def get_regions(self) -> List[pos_structs.RegionResponseStruct]:
        response_data: dict = self.http_client.get_regions_list().json()
        regions: List[pos_structs.RegionResponseStruct] = list()
        for region in response_data:
            regions.append(pos_structs.RegionResponseStruct.from_dict(region))

        return regions

    def get_subjects(self) -> List[pos_structs.SubjectResponseStruct]:
        response_data: dict = self.http_client.get_subjects_list_full().json()[
            "content"
        ]
        subjects: List[pos_structs.SubjectResponseStruct] = list()
        for subject in response_data:
            subjects.append(pos_structs.SubjectResponseStruct.from_dict(subject))

        return subjects

    def get_subsubjects(self) -> List[pos_structs.SubSubjectResponseStruct]:
        response_data: dict = self.http_client.get_subsubjects_list().json()["content"]
        subsubjects: List[pos_structs.SubSubjectResponseStruct] = list()
        for subsubject in response_data:
            subsubjects.append(
                pos_structs.SubSubjectResponseStruct.from_dict(subsubject)
            )

        return subsubjects

    def get_appeal(self, appeal_id) -> pos_structs.AppealResponseStruct:
        response_data: dict = self.http_client.get_appeal_data(appeal_id).json()
        appeal = pos_structs.AppealResponseStruct.from_dict(response_data)
        return appeal

    def add_appeal(
        self, appeal: pos_structs.AppealDataStruct
    ) -> pos_structs.AppealResponseStruct:
        response_data: dict = self.http_client.add_appeal(appeal.to_dict()).json()
        return pos_structs.AppealResponseStruct.from_dict(response_data)

    def send_files(self, files: Iterable[File]) -> Iterable[File]:
        for file in files:
            response_data = self.http_client.send_file(file.file.open("rb")).json()
            pos_id = response_data.get("id")
            file.pos_id = pos_id
        File.objects.bulk_update(files, fields=["pos_id"])
        return files
