import collections

from django.db import models

from modules.core.models import DepartmentStatus


class LivabilityLevelEnum(object):
    COMFORTABLE = "COMFORTABLE"
    UNCOMFORTABLE = "UNCOMFORTABLE"

    RESOLVER = collections.OrderedDict(
        [
            (COMFORTABLE, "Благоустроенная"),
            (UNCOMFORTABLE, "Не благоустроенная"),
        ]
    )

    CHOICES = RESOLVER.items()


class YesNoEnum(object):
    YES = "YES"
    NO = "NO"

    RESOLVER = collections.OrderedDict(
        [
            (YES, "Да"),
            (NO, "Нет"),
        ]
    )

    CHOICES = RESOLVER.items()


class TechnicalStatusEnum(object):
    GOOD = "GOOD"
    SATISFACTORY = "SATISFACTORY"
    UNSATISFACTORY = "UNSATISFACTORY"

    RESOLVER = collections.OrderedDict(
        [
            (GOOD, "Хорошее"),
            (SATISFACTORY, "Удовлетворительное"),
            (UNSATISFACTORY, "Неудовлетворительное"),
        ]
    )

    CHOICES = RESOLVER.items()


# todo: сделай эту модель правильно
class Passport(models.Model):
    department = models.ForeignKey(
        to="core.Department",
        verbose_name="Ведомство",
        related_name="public_territory_improvement_passports",
        on_delete=models.CASCADE,
        limit_choices_to={'status': DepartmentStatus.IS_ACTIVE}
    )

    inventory_date = models.DateField(
        verbose_name="Дата проведения инвентаризации",
    )

    locality_name = models.TextField(
        verbose_name="Населенный пункт",
    )

    real_location = models.TextField(
        verbose_name="Физическое расположение общественной территории",
    )

    name = models.TextField(
        verbose_name="Наименование общественной территории",
    )

    total_area = models.PositiveIntegerField(
        verbose_name="Общая площадь общественной территории, кв. м",
    )

    purpose = models.TextField(
        verbose_name="Назначение",
    )

    cadastral_number = models.TextField(
        verbose_name="Кадастровый номер земельного участка (дворовой территории)",
    )

    livability_level = models.TextField(
        verbose_name="Оценка уровня благоустроенности территории",
        choices=LivabilityLevelEnum.CHOICES,
    )

    people_number_has_comfortable_access = models.PositiveIntegerField(
        verbose_name="Численность населения, имеющая удобный пешеходный доступ к основным площадкам территории, чел.",
    )

    extraneous_presence = models.TextField(
        verbose_name="Наличие объектов недвижимого имущества, незавершенного строительства, земельных участков в собственности (пользовании) юридических лиц и индивидуальных предпринимателей",
    )

    # Характеристики

    # Освещение ####################################
    illumination_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    illumination_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    illumination_elements_number = models.PositiveIntegerField(
        verbose_name="Количество элементов (ед.)",
        null=True,
        blank=True,
    )
    illumination_elements_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    illumination_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Техническое состояние",
        null=True,
        blank=True,
    )
    illumination_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    illumination_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    illumination_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Скамейки #####################################
    benches_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    benches_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    benches_number = models.PositiveIntegerField(
        verbose_name="Количество",
        null=True,
        blank=True,
    )
    benches_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    benches_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Техническое состояние",
        null=True,
        blank=True,
    )
    benches_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    benches_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    benches_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Урны для мусора ##############################
    trash_cans_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    trash_cans_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    trash_cans_number = models.PositiveIntegerField(
        verbose_name="Количество",
        null=True,
        blank=True,
    )
    trash_cans_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    trash_cans_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Техническое состояние",
        null=True,
        blank=True,
    )
    trash_cans_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    trash_cans_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    trash_cans_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Дорожное покрытие ############################
    road_surface_technical_status = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Состояние (требует ремонта/не требует)",
        null=True,
        blank=True,
    )
    road_surface_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Контейнерная площадка ########################
    container_platform_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    container_platform_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Пешеходная дорожка ###########################
    walking_path_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    walking_path_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    walking_path_repairs_needed = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Потребность в ремонте",
        null=True,
        blank=True,
    )
    walking_path_repairs_needed_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Десткие игровые площадки #####################
    playground_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    playground_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    playground_name = models.TextField(
        verbose_name="Наименование",
        blank=True,
    )
    playground_name_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    playground_number = models.PositiveIntegerField(
        verbose_name="Количество",
        null=True,
        blank=True,
    )
    playground_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    playground_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Техническое состояние",
        null=True,
        blank=True,
    )
    playground_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    playground_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    playground_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Спортивные площадки ##########################
    sportsground_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    sportsground_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    sportsground_name = models.TextField(
        verbose_name="Наименование",
        blank=True,
    )
    sportsground_name_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    sportsground_number = models.PositiveIntegerField(
        verbose_name="Количество",
        null=True,
        blank=True,
    )
    sportsground_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    sportsground_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Техническое состояние",
        null=True,
        blank=True,
    )
    sportsground_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    sportsground_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    sportsground_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Места для отдыха #############################
    vacation_spot_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    vacation_spot_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    vacation_spot_name = models.TextField(
        verbose_name="Наименование",
        blank=True,
    )
    vacation_spot_name_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    vacation_spot_number = models.PositiveIntegerField(
        verbose_name="Количество",
        null=True,
        blank=True,
    )
    vacation_spot_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    vacation_spot_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Техническое состояние",
        null=True,
        blank=True,
    )
    vacation_spot_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    vacation_spot_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    vacation_spot_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Зеленые зоны #################################
    green_area_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    green_area_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    green_area_name = models.TextField(
        verbose_name="Наименование",
        blank=True,
    )
    green_area_name_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    green_area_number = models.PositiveIntegerField(
        verbose_name="Количество",
        null=True,
        blank=True,
    )
    green_area_number_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    green_area_technical_status = models.TextField(
        choices=TechnicalStatusEnum.CHOICES,
        verbose_name="Состояние",
        null=True,
        blank=True,
    )
    green_area_technical_status_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    green_area_sufficiently = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Достаточно",
        null=True,
        blank=True,
    )
    green_area_sufficiently_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Приспособления для маломобильных групп #######
    lowmobility_groups_facilities_availability = models.TextField(
        choices=YesNoEnum.CHOICES,
        verbose_name="Наличие",
        null=True,
        blank=True,
    )
    lowmobility_groups_facilities_availability_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    # Иное #########################################
    others = models.TextField(
        verbose_name="Иное",
        blank=True,
    )
    others_note = models.TextField(
        verbose_name="Примечание",
        blank=True,
    )

    class Meta:
        verbose_name = "Паспорт благоустройства общественной территории"
        verbose_name_plural = "Паспорта благоустройства общественных территорий"
