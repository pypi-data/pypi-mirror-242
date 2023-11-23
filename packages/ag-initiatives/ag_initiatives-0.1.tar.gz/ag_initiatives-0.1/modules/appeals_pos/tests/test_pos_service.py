from unittest.mock import patch

from django.test import TestCase

from modules.appeals_pos.services import PosService, pos_structs


class MockResponse:
    def __init__(self, json_data: dict, status_code: int):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestPosService(TestCase):
    pos_service = PosService()

    @patch("modules.appeals_pos.services.PosService.http_client.add_appeal")
    def test_add_appeal(self, client_mock):
        client_mock.return_value = MockResponse(
            {
                "id": None,
                "posId": 563007392,
                "applicant": {
                    "epguId": 1020240201,
                    "surname": "Слепцов",
                    "name": "Олег",
                    "patronymic": "Игоревич",
                    "birthDate": None,
                    "postAddress": None,
                    "postAddressFlat": None,
                    "email": "testtestmail@cifra-k.ru",
                    "phone": None,
                    "snils": None,
                    "omsPolicy": None,
                },
                "description": "test text",
                "attachmentIds": None,
                "location": "fdsfs",
                "subjectId": 125,
                "subsubjectId": 157,
                "factId": None,
                "customFieldValues": [],
                "opaId": 725756,
                "organizationInfo": None,
                "createdAt": "2022-02-21T08:25:50.155509Z",
                "status": "MODERATION_NEW",
                "statusText": "На модерации",
                "history": None,
                "answerAt": None,
                "warnings": [],
            },
            200,
        )

        result = self.pos_service.add_appeal(
            pos_structs.AppealDataStruct(
                description="asda",
                createdAt="fdsfs",
                applicant=pos_structs.ApplicantDataStruct(
                    epguId=1, name="gdfgd", email="aaa@mail.ru"
                ),
            )
        )

        expected_data = pos_structs.AppealResponseStruct(
            pos_id=563007392,
            status="MODERATION_NEW",
            status_text="На модерации",
            history=[],
        )

        self.assertDictEqual(result.dict(), expected_data.dict())

    @patch("modules.appeals_pos.services.PosService.http_client.get_appeal_data")
    def test_get_appeal(self, client_mock):
        client_mock.return_value = MockResponse(
            {
                "id": None,
                "posId": 563007235,
                "applicant": {
                    "epguId": 1020240201,
                    "surname": "Слепцов",
                    "name": "Олег",
                    "patronymic": "Игоревич",
                    "birthDate": None,
                    "postAddress": None,
                    "postAddressFlat": None,
                    "email": "testtestmail@cifra-k.ru",
                    "phone": None,
                    "snils": None,
                    "omsPolicy": None,
                },
                "description": "test text",
                "attachmentIds": [],
                "location": "fdsfs",
                "subjectId": 125,
                "subsubjectId": 157,
                "factId": None,
                "opaId": 725704,
                "organizationInfo": {
                    "opaId": 725704,
                    "name": "АДМИНИСТРАЦИЯ БОГОТОЛЬСКОГО РАЙОНА КРАСНОЯРСКОГО КРАЯ",
                    "address": "662060 г Боготол ул Комсомольская д 2",
                    "regions": None,
                    "subjects": None,
                    "inn": "2406000492",
                    "kpp": "244401001",
                    "ogrn": "1022401224042",
                    "oktmo": "04706000001",
                    "phone": None,
                    "position": None,
                    "email": "",
                },
                "createdAt": "2022-02-14T08:03:56.863875Z",
                "status": "MODERATION_NEW",
                "statusText": "На модерации",
                "history": [
                    {
                        "status": "MODERATION_NEW",
                        "statusText": "На модерации",
                        "answer": None,
                        "createdAt": "2022-02-14T08:03:56.969310Z",
                        "createdBy": {
                            "surname": "Внешняя",
                            "name": "Система",
                            "patronymic": "Приема Сообщений",
                            "position": None,
                            "email": None,
                            "phone": None,
                        },
                    }
                ],
                "answerAt": "2022-03-16T08:03:56.966669Z",
                "warnings": None,
            },
            200,
        )

        appeal: pos_structs.AppealResponseStruct = self.pos_service.get_appeal(24)
        expected_data = pos_structs.AppealResponseStruct(
            pos_id=563007235,
            status="MODERATION_NEW",
            status_text="На модерации",
            history=[
                pos_structs.HistoryStruct(
                    status="MODERATION_NEW",
                    status_text="На модерации",
                    answer=None,
                    created_at="2022-02-14T08:03:56.969310Z",
                    created_by=pos_structs.HistoryCreatedByStruct(
                        surname="Внешняя",
                        name="Система",
                        patronymic="Приема Сообщений",
                        position=None,
                        email=None,
                        phone=None,
                    ),
                )
            ],
        )

        self.assertDictEqual(appeal.to_dict(), expected_data.to_dict())

    @patch("modules.appeals_pos.services.PosService.http_client.get_subjects_list_full")
    def test_get_subjects(self, client_mock):
        client_mock.return_value = MockResponse(
            {
                "content": [
                    {
                        "id": 119,
                        "name": "Образование",
                        "deleted": False,
                    },
                    {
                        "id": 115,
                        "name": "Благоустройство",
                        "deleted": False,
                    },
                    {
                        "id": 116,
                        "name": "Дворы и территории общего пользования",
                        "deleted": False,
                    },
                ]
            },
            200,
        )

        data = self.pos_service.get_subjects()
        expected_data = [
            pos_structs.SubjectResponseStruct(id=119, name="Образование"),
            pos_structs.SubjectResponseStruct(id=115, name="Благоустройство"),
            pos_structs.SubjectResponseStruct(
                id=116, name="Дворы и территории общего пользования"
            ),
        ]

        self.assertListEqual(
            [subject.to_dict() for subject in data],
            [expected.to_dict() for expected in expected_data],
        )

    @patch("modules.appeals_pos.services.PosService.http_client.get_subsubjects_list")
    def test_get_subsubjects(self, client_mock):
        client_mock.return_value = MockResponse(
            {
                "content": [
                    {
                        "id": 119,
                        "name": "Образование",
                        "deleted": False,
                        "subject": {
                            "id": 349,
                            "name": "Тестовая0911v2",
                        },
                    },
                    {
                        "id": 115,
                        "name": "Благоустройство",
                        "deleted": False,
                        "subject": {
                            "id": 349,
                            "name": "Тестовая0911v2",
                        },
                    },
                ]
            },
            200,
        )

        data = self.pos_service.get_subsubjects()
        subject_struct = pos_structs.SubjectResponseStruct(
            id=349, name="Тестовая0911v2"
        )
        expected_data = [
            pos_structs.SubSubjectResponseStruct(
                id=119, name="Образование", subject=subject_struct
            ),
            pos_structs.SubSubjectResponseStruct(
                id=115, name="Благоустройство", subject=subject_struct
            ),
        ]

        self.assertListEqual(
            [subsubject.to_dict() for subsubject in data],
            [expected.to_dict() for expected in expected_data],
        )
