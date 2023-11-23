from django.test.testcases import TestCase

from modules.core.models import OperatorLkoPermissions, User, SubPermissions, Department, Locality, Category
from modules.core.models.permissions import ModulesPermissions
from modules.core.services.operator_lko import OperatorLkoService
from modules.initiatives.models import InitiativeCategory
from modules.map_works.models import WorkCategory
from modules.plans.models import Category as PlanCategory


def create_categories():
    Category.objects.create(name='Голосование')
    InitiativeCategory.objects.create(name='Инициатива')
    WorkCategory.objects.create(name='Ремонтные работы, карта')
    PlanCategory.objects.create(name='Планы')


def create_user_and_sub_permission():
    User.objects.create(first_name="test_User", roles=["OPERATOR_LKO"])
    SubPermissions.objects.create(user=User.objects.first())


def create_locality_and_return_department():
    Locality.objects.create(name='МО или НП', type=10)
    locality = Locality.objects.all()
    Department.objects.create(
        name='Администрация',
        email='department@mail.ru',
        image=None
    )
    department: Department = Department.objects.first()
    department.locality.set(locality)
    department.save()
    return department


def create_operator_permission():
    create_categories()
    create_user_and_sub_permission()
    department = create_locality_and_return_department()

    OperatorLkoPermissions.objects.create(
        user_sub_permissions=SubPermissions.objects.first(),
        modules_permissions="MAP_WORKS",
        department=department
    )
    operator_permission: OperatorLkoPermissions = OperatorLkoPermissions.objects.first()
    locality = Locality.objects.all()
    operator_permission.initiatives_categories.set(InitiativeCategory.objects.all())
    operator_permission.initiatives_localities.set(locality)
    operator_permission.initiatives_municipalities.set(locality)

    operator_permission.voting_categories.set(Category.objects.all())
    operator_permission.voting_localities.set(locality)
    operator_permission.voting_municipalities.set(locality)

    operator_permission.plans_categories.set(PlanCategory.objects.all())
    operator_permission.plans_localities.set(locality)
    operator_permission.plans_municipalities.set(locality)

    operator_permission.map_works_categories.set(WorkCategory.objects.all())
    operator_permission.map_works_localities.set(locality)
    operator_permission.map_works_municipalities.set(locality)
    operator_permission.save()
    return operator_permission


class OperatorPermissionTestCase(TestCase):

    def setUp(self):
        self.operator_permission = create_operator_permission()
        user = User.objects.first()
        self.services = {
            "INITIATIVES": OperatorLkoService(user=user, module=ModulesPermissions.INITIATIVES),
            "MAP_WORKS": OperatorLkoService(user=user, module=ModulesPermissions.MAP_WORKS),
            "VOTING": OperatorLkoService(user=user, module=ModulesPermissions.VOTING),
            "PLANS": OperatorLkoService(user=user, module=ModulesPermissions.PLANS)
        }

    def test_operator_lko_get_allowed_departments(self):
        department = Department.objects.first()
        for service in self.services.values():
            with self.subTest(service=service):
                self.assertEqual(service.get_allowed_departments().pop(), department)

    def test_operator_lko_get_allowed_localities(self):
        locality = Locality.objects.first()
        for service in self.services.values():
            with self.subTest(service=service):
                self.assertEqual(service.get_allowed_localities().pop(), locality)

    def test_operator_lko_get_allowed_categories(self):
        category = {
            "MAP_WORKS": WorkCategory.objects.first(),
            "VOTING": Category.objects.first(),
            "INITIATIVES": InitiativeCategory.objects.first(),
            "PLANS": PlanCategory.objects.first()
        }

        for module, category in category.items():
            with self.subTest(module=module):
                service: OperatorLkoService = self.services[module]
                self.assertEqual(service.get_allowed_categories().first(), category)
