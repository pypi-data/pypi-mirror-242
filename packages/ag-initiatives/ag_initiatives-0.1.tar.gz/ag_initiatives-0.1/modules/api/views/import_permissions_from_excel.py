import base64
from io import BytesIO

import pandas as pd
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from config.settings.celery import app
from ...core.models import Locality, User, Department, DepartmentSubPermissions, Category as CoreCategory, \
    AdminLkoPermissions, OperatorLkoPermissions, SubPermissions, UserRole
from ...core.models.permissions import ModulesPermissions
from ...ecology.models import EventCategory, GoodsNServicesItemCategory
from ...feedback.models import Problematic
from ...initiatives.models import InitiativeCategory
from ...map_works.models import WorkCategory
from ...plans.models import Category as PlansCategory


def get_str(s):
    if pd.isnull(s):
        return ''
    return s


@app.task
def async_import_permissions_from_excel(file_data_base64):
    file_data = base64.b64decode(file_data_base64)
    file = BytesIO(file_data)

    xl = pd.read_excel(file, 'Ответственные', engine='openpyxl')

    for i in range(0, len(xl)):
        row = xl.loc[i]
        try:
            fio = [i.strip() for i in get_str(row['ФИО']).split()]
            try:
                users = User.objects.filter(last_name__iexact=fio[0], first_name__iexact=fio[1], patronymic_name__iexact=fio[2])
            except IndexError:
                continue
            for user in users:
                roles = [i.strip().lower() for i in get_str(row['Роль']).split(',')] + ["пользователь"]
                user.roles = [
                    k for k, v in UserRole.RESOLVER.items() if v.lower() in roles
                ]
                user.save()
                department, department_create = Department.objects.get_or_create(
                    name=get_str(row['Организация']),
                    defaults={
                        'email': '-',
                        'email_initiative_notification': False,
                    }
                )
                if name := get_str(row['Вышестоящая организация']):
                    department_parent, _ = Department.objects.get_or_create(
                        name=name,
                        defaults={
                            'email': '-',
                            'email_initiative_notification': False,
                        }
                    )
                    department.parent = department_parent
                    department.save()

                department_sub_permissions, sub_permissions_create = DepartmentSubPermissions.objects.get_or_create(
                    department=department,
                    defaults={
                        'modules_permissions': [],
                    }
                )
                if sub_permissions_create:
                    department_sub_permissions.modules_permissions = ['MAP_WORKS', "PLANS", "VOTING", "INITIATIVES",
                                                                      "APPEALS",
                                                                      "ENCOURAGEMENTS",
                                                                      "SUGGESTIONS"]
                    department_sub_permissions.voting_categories.set(CoreCategory.objects.all())
                    department_sub_permissions.initiative_categories.set(InitiativeCategory.objects.all())
                    department_sub_permissions.map_works_categories.set(WorkCategory.objects.all())
                    department_sub_permissions.plans_categories.set(PlansCategory.objects.all())
                    department_sub_permissions.appeals_categories.set(Problematic.objects.all())
                    department_sub_permissions.suggestion_categories.set(EventCategory.objects.all())
                    department_sub_permissions.encouragement_categories.set(GoodsNServicesItemCategory.objects.all())
                localities = []
                if department_create:
                    if 'все' == get_str(row['МО для Вашего мнения']).strip().lower():
                        department.locality.set(Locality.objects.all())
                    else:
                        mo = [i.strip() for i in get_str(row['МО для Вашего мнения']).split(',')]
                        for m in mo:
                            if not m:
                                continue
                            locality, _ = Locality.objects.get_or_create(name=m)
                            localities.append(locality)
                        department.locality.set(localities)
                user.department = department
                user.save()

                if user.is_admin_lko:
                    admin_lko_permissions, _ = AdminLkoPermissions.objects.get_or_create(
                        user=user,
                        defaults={
                            'department': department,
                        }
                    )
                    admin_lko_permissions.department = department
                    sub_permissions, _ = SubPermissions.objects.get_or_create(user=user)
                    admin_lko_permissions.sub_permissions = sub_permissions
                    admin_lko_permissions.save()
                if user.is_operator:
                    operator_lko_permissions, _ = OperatorLkoPermissions.objects.get_or_create(
                        user=user,
                        defaults={
                            'department': department,
                            'modules_permissions': [],
                        }
                    )
                    operator_lko_permissions.department = department
                    if 'все' == get_str(row['МО для Вашего мнения']).strip().lower():
                        operator_lko_permissions.voting_localities.set(department.locality.all())
                        operator_lko_permissions.initiatives_localities.set(department.locality.all())
                        operator_lko_permissions.map_works_localities.set(department.locality.all())
                        operator_lko_permissions.plans_localities.set(department.locality.all())
                        operator_lko_permissions.appeals_localities.set(Locality.objects.all())
                        operator_lko_permissions.suggestion_localities.set(department.locality.all())
                        operator_lko_permissions.encouragement_localities.set(department.locality.all())
                    else:
                        mo = [i.strip() for i in get_str(row['МО для Вашего мнения']).split(',')]
                        for m in mo:
                            if not m:
                                continue
                            locality, _ = Locality.objects.get_or_create(name=m)
                            localities.append(locality)
                        operator_lko_permissions.voting_localities.set(department.locality.all())
                        operator_lko_permissions.initiatives_localities.set(department.locality.all())
                        operator_lko_permissions.map_works_localities.set(department.locality.all())
                        operator_lko_permissions.plans_localities.set(department.locality.all())
                        operator_lko_permissions.appeals_localities.set(localities)
                        operator_lko_permissions.suggestion_localities.set(department.locality.all())
                        operator_lko_permissions.encouragement_localities.set(department.locality.all())

                    operator_lko_permissions.map_works_categories.set(WorkCategory.objects.all())
                    operator_lko_permissions.plans_categories.set(PlansCategory.objects.all())

                    if 'все' == get_str(row['Категории  голосований']).strip().lower():
                        operator_lko_permissions.voting_categories.set(CoreCategory.objects.all())
                    else:
                        mo = [i.strip() for i in get_str(row['Категории  голосований']).split(',')]
                        categories = [CoreCategory.objects.get_or_create(name=m) for m in mo if m]
                        operator_lko_permissions.voting_categories.set([i for i, _ in categories])
                    if 'все' == get_str(row['Категории инициатив']).strip().lower():
                        operator_lko_permissions.initiatives_categories.set(InitiativeCategory.objects.all())
                    else:
                        a = [i.strip() for i in get_str(row['Категории инициатив']).split(',')]
                        b = [i.strip() for i in get_str(row['Подкатегории инициатив']).split(',')]
                        categories = [InitiativeCategory.objects.get_or_create(name=m) for m in set(a + b) if m]
                        operator_lko_permissions.initiatives_categories.set([i for i, _ in categories])
                    if 'все' == get_str(row['Ваше мнение Проблематика']).strip().lower():
                        operator_lko_permissions.appeals_categories.set(Problematic.objects.all())
                    else:
                        mo = [i.strip() for i in get_str(row['Ваше мнение Проблематика']).split(',')]
                        categories = [Problematic.objects.get_or_create(name=m) for m in mo if m]
                        operator_lko_permissions.appeals_categories.set([i for i, _ in categories])
                    if 'все' == get_str(row['Предложения Тематическая\nкатегория']).strip().lower():
                        operator_lko_permissions.suggestion_categories.set(EventCategory.objects.all())
                    else:
                        mo = [i.strip() for i in get_str(row['Предложения Тематическая\nкатегория']).split(',')]
                        categories = [EventCategory.objects.get_or_create(name=m) for m in mo if m]
                        operator_lko_permissions.suggestion_categories.set([i for i, _ in categories])
                    if 'все' == get_str(row['Поощрения Тематическая\nкатегория']).strip().lower():
                        operator_lko_permissions.encouragement_categories.set(GoodsNServicesItemCategory.objects.all())
                    else:
                        mo = [i.strip() for i in get_str(row['Поощрения Тематическая\nкатегория']).split(',')]
                        categories = [GoodsNServicesItemCategory.objects.get_or_create(name=m) for m in mo if m]
                        operator_lko_permissions.encouragement_categories.set([i for i, _ in categories])

                    sub_permissions, _ = SubPermissions.objects.get_or_create(user=user)
                    operator_lko_permissions.user_sub_permissions = sub_permissions
                    modules_permissions = [i.strip().lower() for i in get_str(row['Разделы']).split(',')]
                    operator_lko_permissions.modules_permissions = [
                        k for k, v in ModulesPermissions.RESOLVER.items() if v.lower() in modules_permissions
                    ]
                    operator_lko_permissions.save()
        except Exception as err:
            print(
                {
                    'row': int(row.name) + 2,
                    'err': str(err)
                }
            )


@api_view(["POST"])
@permission_classes([IsAdminUser])
def import_permissions_from_excel(request):
    file = request.data['file']
    file_data = file.read()
    file_data_base64 = base64.b64encode(file_data).decode('utf-8')
    async_import_permissions_from_excel.delay(file_data_base64)
    return Response({}, status=status.HTTP_204_NO_CONTENT)
