from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils import timezone
from modules.core.models import UserRole
from modules.plans.models import (
    Category,
    DepartmentCategory,
    Location,
    Plan,
    PlanComment,
    FileType,
    File,
)

User = get_user_model()


class PlansTestCase(APITestCase):
    def setUp(self) -> None:
        # self.admin = User.objects.create_user(
        #     username='admin123', password='123', roles=UserRole.ADMIN_LKO
        # )
        self.operator = User.objects.create_user(
            username='admin1234', password='1234', roles=UserRole.OPERATOR_LKO
        )
        # self.user = User.objects.create_user(
        #     userneme='admin12345', password='12345', roles=UserRole.USER
        # )
        # self.token_admin = Token.objects.get_or_create(user=self.admin)[0]
        self.token_operator = Token.objects.get_or_create(user=self.operator)[0]
        # self.token_user = Token.objects.get_or_create(user=self.user)[0]

    def set_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token{token}")

    def create_list_plans(self, owner):
        owner = owner.objects.create(name='Owner')
        plans = Plan.objects.create(name='Plans')
        category = Category.objects.create(
            name='name',
            color="#000000",
            image=None,
            icon='Иконка',
        )
        category_department = DepartmentCategory.objects.create(
            department=DepartmentCategory,
            category=Category,
        )
        comments = PlanComment.objects.create(
            plan=plans,
            text="Текст",
            timestamp=timezone.now(),
            user=User,
            moderated='Модерация пройдена',
        )

        plan = plans.objects.create(
            name='name',
            locality='Муниципальное образование',
            category=category,
            publication_date='Дата изменения',
            discription='Описание',
            location=Location,
            files=File,
            owner=owner,
        )
        file = File.objects.create(
            file='Файл',
            type=FileType,
            name='name',
            order='Порядок',
            owner=owner,
        )

    # operator
    def test_list_accept_category_department(self):
        category_department = self.create_list_plans(self.operator)
        url = reverse('category_department-private-accept-operator')
        self.set_credentials(self.token_operator)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(category_department, DepartmentCategory)

    def test_operator_create_plan(self):
        url = reverse('category_department-private-reject-operator')
        self.set_credentials(self.token_operator)
        expected_data = {
            {
                "id": 14,
                "name": "fdasklfsdad",
                "locality": 77,
                "category": 7,
                "publication_date": "2022-07-14",
                "description": "kjflsdkjglas",
                "location": {
                    "address": "ул. Игарская, 6",
                    "gis_point": {
                        "type": "Point",
                        "coordinates": [
                            56.020207844199774,
                            92.88744001512076
                        ]
                    },
                    "gis_polygon": null
                },
                "files": [
                    {
                        "id": 30,
                        "link": "/media/plans/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA_%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0_%D0%BE%D1%82_2022-07-05_14-57-31_Y7R9Hap.png",
                        "type": "IMAGE",
                        "order": null,
                        "name": "IMAGE от 2022-07-05 14-57-31.png"
                    }
                ],
                "comments": []
            }
        }
        input_data = {
            {
                "name": "fdasklfsdad",
                "locality": 77,
                "category": 7,
                "publication_date": "2022-07-14",
                "description": "kjflsdkjglas",
                "location": {
                    "address": "ул. Игарская, 6",
                    "gis_point": {
                        "type": "Point",
                        "coordinates": [
                            56.020207844199774,
                            92.88744001512076
                        ]
                    },
                    "gis_polygon": null
                },
                "files": [
                    30
                ]
            }
        }

        response = self.client.post(url, data=input_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_data, response.body)
