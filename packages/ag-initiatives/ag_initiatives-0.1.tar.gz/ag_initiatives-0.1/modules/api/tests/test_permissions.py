import os

from django.contrib.auth import get_user_model
from django.core.files import File
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from modules.core.models import UserRole, Department
from modules.initiatives.models import (
    Initiative,
    InitiativeCategory,
    InitiativeState,
    InitiativeAcceptingSettings,
    InitiativeRejectReason,
    InitiativeFile,
    InitiativeFileType,
)
from modules.voting.factories.vote import LocalityFactory

User = get_user_model()


class PermissionsTestCase(APITestCase):
    def setUp(self) -> None:
        self.locality = LocalityFactory.create()
        self.locality_2 = LocalityFactory.create()
        self.moderator = User.objects.create_user(
            username="root1", password="123", roles=UserRole.MODERATOR
        )
        self.applicant = User.objects.create_user(
            username="root12", password="123", roles=UserRole.USER
        )
        self.operator = User.objects.create_user(
            username="root123", password="123", roles=UserRole.OPERATOR
        )
        self.token_moderator = Token.objects.get_or_create(user=self.moderator)[0]
        self.token_applicant = Token.objects.get_or_create(user=self.applicant)[0]
        self.token_operator = Token.objects.get_or_create(user=self.operator)[0]

    def set_credentials(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def create_initiative(self, user, state=InitiativeState.PREMODERATION):
        category = InitiativeCategory.objects.create(name="CATEGORY")
        department = Department.objects.create(
            name="name",
            email="asadsa@mail.ru",
        )
        department.locality.set([self.locality])
        settings = InitiativeAcceptingSettings.objects.create(
            department=department,
            locality=self.locality,
            category=category,
            duration_month=10,
            votes_threshold=10,
            active=True,
        )
        initiative = Initiative.objects.create(
            title="TITLE",
            number="NUMBER",
            creation_date_time=timezone.now(),
            user=user,
            email="asadsa@mail.ru",
            category=category,
            locality=self.locality,
            state=state,
            settings=settings,
            duration_month=10,
            votes_threshold=10,
            description="DESCRIPTION",
            expectations="DESCRIPTION",
        )
        self.moderator.department = department
        self.moderator.save()
        self.operator.department = department
        self.operator.save()
        return initiative

    def test_applicant_cant_accept_premoderation(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-accept-moderator", args=(initiative.pk,))
        self.set_credentials(self.token_applicant)
        response = self.client.post(url)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.PREMODERATION)

    def test_applicant_cant_reject_premoderation(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-reject-moderator", args=(initiative.pk,))
        self.set_credentials(self.token_applicant)
        response = self.client.post(url)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.PREMODERATION)

    def test_applicant_cant_offer_changes(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-change-moderator", args=(initiative.pk,))
        data = {
            "title": "NEW TITL11E",
            "description": "NEW_DESCRIPTION",
            "expectations": "NOTHING",
        }
        self.set_credentials(self.token_applicant)
        response = self.client.put(url, data=data)

        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

    def test_applicant_can_reject_changes(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-change-moderator", args=(initiative.pk,))
        data = {
            "title": "NEW TITL11E",
            "description": "NEW_DESCRIPTION",
            "expectations": "NOTHING",
        }
        self.set_credentials(self.token_moderator)
        response = self.client.put(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.CHANGES_APPROVAL)

        url = reverse("initiative-private-reject-user", args=(initiative.pk,))
        self.set_credentials(self.token_applicant)
        response = self.client.post(url)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.REJECTED)

    def test_applicant_can_accept_changes(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-change-moderator", args=(initiative.pk,))
        data = {
            "title": "NEW TITL11E",
            "description": "NEW_DESCRIPTION",
            "expectations": "NOTHING",
        }
        self.set_credentials(self.token_moderator)
        response = self.client.put(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.CHANGES_APPROVAL)

        url = reverse("initiative-private-accept-user", args=(initiative.pk,))
        self.set_credentials(self.token_applicant)
        response = self.client.post(url)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.MODERATION)

    def test_applicant_and_moderator_can_message_each_other_without_changing_state(
        self,
    ):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-request-info", args=(initiative.pk,))
        data = {"text": "how are u, mister user?"}
        self.set_credentials(self.token_moderator)
        response = self.client.post(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.PREMODERATION)

        data = {"text": "Hello, ok and u, mister moderator?"}
        url = reverse("initiative-private-response-info", args=(initiative.pk,))
        self.set_credentials(self.token_applicant)
        response = self.client.post(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.PREMODERATION)


    def test_moderator_can_reject_premoderation(self):
        initiative = self.create_initiative(self.applicant)
        reason = InitiativeRejectReason.objects.create(text="reject_reason")
        data = dict(reason=reason.pk)
        url = reverse("initiative-private-reject-moderator", args=(initiative.pk,))
        self.set_credentials(self.token_moderator)
        response = self.client.post(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(initiative.state, InitiativeState.REJECTED)

    def test_moderator_can_accept_premoderation(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-accept-moderator", args=(initiative.pk,))
        self.set_credentials(self.token_moderator)
        response = self.client.post(url)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(initiative.state, InitiativeState.MODERATION)

    def test_moderator_can_offer_changes_only_once(self):
        initiative = self.create_initiative(self.applicant)
        url = reverse("initiative-private-change-moderator", args=(initiative.pk,))
        data = {
            "title": "NEW TITL11E",
            "description": "NEW_DESCRIPTION",
            "expectations": "NOTHING",
        }
        self.set_credentials(self.token_moderator)
        self.assertEqual(initiative.state, InitiativeState.PREMODERATION)
        response = self.client.put(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(initiative.state, InitiativeState.CHANGES_APPROVAL)

        response = self.client.put(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(initiative.state, InitiativeState.CHANGES_APPROVAL)


    def test_operator_can_reject(self):
        initiative = self.create_initiative(self.applicant, InitiativeState.MODERATION)
        reason = InitiativeRejectReason.objects.create(text="reject_reason")
        url = reverse("initiative-private-reject-operator", args=(initiative.pk,))
        self.set_credentials(self.token_operator)
        data = {"text": "rejection text"}
        response = self.client.post(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(initiative.state, InitiativeState.REJECTED)

    def test_operator_can_accept(self):
        initiative = self.create_initiative(self.applicant, InitiativeState.MODERATION)
        url = reverse("initiative-private-accept-operator", args=(initiative.pk,))
        self.set_credentials(self.token_operator)
        response = self.client.post(url)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(initiative.state, InitiativeState.VOTES_COLLECTION)

    def test_operator_can_publish_decision(self):
        initiative = self.create_initiative(
            self.applicant, InitiativeState.CONSIDERATION
        )
        url = reverse("initiative-private-publish", args=(initiative.pk,))
        self.set_credentials(self.token_operator)
        data = {"text": "publish"}
        response = self.client.post(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(initiative.state, InitiativeState.IN_PROGRESS)

    def test_operator_can_accomplish(self):
        initiative = self.create_initiative(self.applicant, InitiativeState.IN_PROGRESS)
        url = reverse("initiative-private-accomplish", args=(initiative.pk,))
        self.set_credentials(self.token_operator)
        data = {"text": "accomplish"}
        response = self.client.post(url, data=data)
        initiative.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(initiative.state, InitiativeState.ACCOMPLISHED)
