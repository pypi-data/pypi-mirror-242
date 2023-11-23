from django.test import TestCase

from modules.subscriptions.tests.common_data_for_tests import (
    Common,
)


class EmailBackendServiceTestCase(TestCase, Common):
    """"""

    @classmethod
    def setUpTestData(cls):
        cls._basic_setup()

    def setUp(self) -> None:
        pass
