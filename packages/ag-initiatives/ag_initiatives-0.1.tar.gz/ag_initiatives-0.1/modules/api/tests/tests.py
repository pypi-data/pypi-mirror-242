import random
import urllib

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from modules.voting.factories.vote import (
    LocalityFactory,
    VoteFactory,
    VoteQuestionFactory,
    VoteAnswerOptionFactory,
    CategoryFactory,
)
from modules.voting.models import VoteQuestion

User = get_user_model()


def build_url(*args, **kwargs):
    get = kwargs.pop("get", {})
    url = reverse(*args, **kwargs)
    if get:
        url += "?" + urllib.parse.urlencode(get)
        return url


class VoteApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.votes_count = 10
        self.questions_in_vote_count = 5
        self.answers_in_question_count = 4
        self.locality = LocalityFactory.create()
        self.locality_2 = LocalityFactory.create()
        self.user = User.objects.create_user(username="root123", password="123")
        self.token = Token.objects.get_or_create(user=self.user)[0]
        self.vote_categories = CategoryFactory.create_batch(size=10)
        self.votes = VoteFactory.create_batch(
            size=self.votes_count,
            locality=(self.locality, self.locality_2),
            category=self.vote_categories[0],
        )
        self.create_questions_and_answers()

    def set_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def make_correct_questions_and_correct_answers(self, vote):
        data = {
            question.id: [
                random.choice(list(question.answers.all().values_list("id", flat=True)))
            ]
            for question in vote.questions.all()
        }
        data.update({"user_locality_id": self.locality.id})
        return data

    def make_correct_questions_and_incorrect_answers(self, vote):
        data = {
            question.id: [random.randint(10000, 20000)]
            for question in vote.questions.all()
        }
        data.update({"user_locality_id": self.locality.id})
        return data

    def create_questions_and_answers(self):
        for vote in self.votes:
            VoteQuestionFactory.create_batch(
                size=self.questions_in_vote_count, vote=vote
            )
        for question in VoteQuestion.objects.all():
            VoteAnswerOptionFactory.create_batch(
                size=self.answers_in_question_count, vote_question=question
            )

    def test_vote_action_without_token(self):
        url = reverse("vote-vote", args=(1,))
        response = self.client.post(url)

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_vote_action_with_token_and_correct_data(self):
        self.set_credentials()
        for vote in self.votes:
            data = self.make_correct_questions_and_correct_answers(vote)
            url = reverse("vote-vote", args=(vote.id,))
            response = self.client.post(url, data=data, format="json")
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_vote_action_with_token_and_wrong_answers(self):
        self.set_credentials()
        for vote in self.votes:
            data = self.make_correct_questions_and_incorrect_answers(vote)
            url = reverse("vote-vote", args=(vote.id,))
            response = self.client.post(url, data=data, format="json")

            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_vote_action_with_token_and_without_user_locality_id(self):
        self.set_credentials()
        for vote in self.votes:
            url = reverse("vote-vote", args=(vote.id,))
            response = self.client.post(url, format="json")
            self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_vote_action_with_token_voting_twice(self):
        self.set_credentials()
        vote = random.choice(self.votes)
        data = self.make_correct_questions_and_correct_answers(vote)
        url = reverse("vote-vote", args=(vote.id,))
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response_second = self.client.post(url, data=data, format="json")

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response_second.status_code)
