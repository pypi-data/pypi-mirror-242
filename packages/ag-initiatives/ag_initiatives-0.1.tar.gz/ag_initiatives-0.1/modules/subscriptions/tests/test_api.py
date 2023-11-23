from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from modules.core.models import User, Locality
from modules.subscriptions.models import Subscription
from modules.subscriptions.tests.common_data_for_tests import Common, ModelCommon


class SubscriptionApiTestCase(APITestCase, ModelCommon):
    class Meta:
        model = Subscription

    @classmethod
    def setUpTestData(cls):
        cls._basic_setup()
        user = User.objects.all().first()
        token = Token.objects.create(user=user)

    def setUp(self) -> None:
        token = Token.objects.all().first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        # self.client.credential(username=f"{token.user.username}", password="simple_password")

    def test_get_list(self):
        response = self.client.get("/api/subscriptions/subscription/")
        self.assertEqual(response.status_code, 200)

    def test_get_retrieve(self):
        self.create_subscription_object()
        subscription = Subscription.objects.all().first()
        response = self.client.get(f"/api/subscriptions/subscription/{subscription.id}")
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        subscription = Subscription.objects.all().first()
        locality = Locality.objects.all().first()
        data = {
            "event": self.subscription_data.get("event"),
            "category": self.subscription_data.get("category"),
            "locality": locality.pk,
        }
        response = self.client.post(f"/api/subscriptions/subscription/", data=data)
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        pass
