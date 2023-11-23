from django.test import TestCase

from modules.appeals_pos.services import PosHttpClient


class TestPosClient(TestCase):

    pos_client = PosHttpClient()

    def test_get_regions_list(self):
        response = self.pos_client.get_regions_list()
        response.raise_for_status()

    def test_get_subjects_list(self):
        response = self.pos_client.get_subjects_list()
        response.raise_for_status()

    def test_get_subjects_list_full(self):
        response = self.pos_client.get_subjects_list()
        response.raise_for_status()

    def test_get_subsubjects_list(self):
        response = self.pos_client.get_subsubjects_list()
        response.raise_for_status()

    def test_add_appeal(self):
        response = self.pos_client.add_appeal(
            {
                "description": "aiswfae yoeygwqoeyrgfewdf",
                "regionId": 24,
                "applicant": {
                    "epguId": 64,
                    "name": "Vasya",
                    "surname": "String",
                    "email": "test@cifra-k.ru",
                    "phone": "6546549625846219",
                },
                "subjectId": 3,
                "subsubjectId": 200,
                "createdAt": "2021-10-11T08:19:23.269Z",
                "id": 124124,
                "location": "dfhsdftghsdf ghsd fgsdfg",
                "organizationInfo": {"ogrn": "1022402674744"},
            }
        )
        response.raise_for_status()

    def test_get_appeal(self):
        response = self.pos_client.get_appeal_data(563007235)
        response.raise_for_status()
