import logging
from typing import List, Iterable

from django.db.models import Q
from django.utils.dateparse import parse_datetime

from modules.appeals_pos.models import (
    Category,
    Subcategory,
    Appeal,
    AppealAnswer,
    AppealStateChange,
)
from modules.appeals_pos.models.appeal import AppealState
from modules.appeals_pos.services.rest import pos_structs
from modules.appeals_pos.services.rest.pos_service import PosService

logger = logging.getLogger("appeals.update")


class UpdatePosService:
    pos_service = PosService()

    @staticmethod
    def _create_category_entity(
        category: pos_structs.SubjectResponseStruct,
    ) -> Category:
        """Создает модель категории из структуры ПОС"""
        return Category(pos_id=category.id, name=category.name)

    @staticmethod
    def _create_subcategory_entity(
        subcategory: pos_structs.SubSubjectResponseStruct,
    ) -> Subcategory:
        """Создает модель подкатегории из структуры ПОС"""
        category = Category.objects.filter(pos_id=subcategory.subject.id).first()
        return Subcategory(
            pos_id=subcategory.id, name=subcategory.name, category=category
        )

    @staticmethod
    def _get_current_categories_pos_ids() -> List[int]:
        """Получить все id категорий из локальной базы"""
        return list(Category.objects.all().values_list("pos_id", flat=True))

    @staticmethod
    def _get_current_subcategories_pos_ids() -> List[int]:
        """Получить все id подкатегорий из локальной базы"""
        return list(Subcategory.objects.all().values_list("pos_id", flat=True))

    def _get_categories_pos_ids(self) -> List[int]:
        """Получить все id категорий из ПОС"""
        categories: List[
            pos_structs.SubjectResponseStruct
        ] = self.pos_service.get_subjects()
        return list(map(lambda category: category.id, categories))

    def _get_subcategories_pos_ids(self) -> List[int]:
        """Получить все id подкатегорий из ПОС"""
        subcategories: List[
            pos_structs.SubSubjectResponseStruct
        ] = self.pos_service.get_subsubjects()
        return list(map(lambda subcategory: subcategory.id, subcategories))

    def _create_categories_entities(
        self, categories_structs: List[pos_structs.SubjectResponseStruct]
    ) -> List[Category]:
        """Создает список моделей категорий из структур ПОС"""
        categories_entities: List[Category] = []
        for category_struct in categories_structs:
            categories_entities.append(self._create_category_entity(category_struct))

        return categories_entities

    def _create_subcategory_entities(
        self, subcategories_struct: List[pos_structs.SubSubjectResponseStruct]
    ) -> List[Subcategory]:
        """Создает список моделей подкатегорий из структур ПОС"""
        subcategories_entities: List[Subcategory] = []
        for subcategory_struct in subcategories_struct:
            subcategories_entities.append(
                self._create_subcategory_entity(subcategory_struct)
            )

        return subcategories_entities

    def _get_all_subcategories_entities_from_pos(self) -> List[Subcategory]:
        """Делает запрос в ПОС на получение подкатегорий и переводит их в модели"""
        subcategories = self.pos_service.get_subsubjects()
        subcategories_entities = self._create_subcategory_entities(subcategories)
        return subcategories_entities

    def _update_deleted_categories(self) -> List[Category]:
        ids = self._get_categories_pos_ids()
        categories_to_update = Category.objects.filter(
            ~Q(pos_id__in=ids) & Q(deleted=False)
        )
        categories_to_update.update(deleted=True)
        return list(categories_to_update)

    def _update_deleted_subcategories(self) -> List[Subcategory]:
        ids = self._get_subcategories_pos_ids()
        subcategories_to_update = Subcategory.objects.filter(
            ~Q(pos_id__in=ids) & Q(deleted=False)
        )
        subcategories_to_update.update(deleted=True)
        return list(subcategories_to_update)

    def _update_appeal(self, appeal: Appeal):
        """Обновляет историю обращения"""
        appeal_struct = self.pos_service.get_appeal(appeal.pos_id)

        appeal.status = AppealState.from_pos_status(appeal_struct.status)
        appeal.save(update_fields=["status"])

        answers_to_create: List[AppealAnswer] = []

        appeal_history = AppealStateChange.objects.filter(appeal=appeal).all()

        for history_struct in appeal_struct.history:

            if parse_datetime(history_struct.created_at) in list(
                map(
                    lambda appeal_state_change: appeal_state_change.created_at,
                    appeal_history,
                )
            ):
                continue

            appeals_state_change = AppealStateChange.objects.create(
                appeal=appeal,
                status=AppealState.from_pos_status(history_struct.status),
                created_at=history_struct.created_at,
                created_by=f"{history_struct.created_by.surname} {history_struct.created_by.name} {history_struct.created_by.patronymic} ",
                pos_status=history_struct.status,
                pos_status_name=history_struct.status_text,
            )

            if history_struct.answer:
                answer = history_struct.answer
                answers_to_create.append(
                    AppealAnswer(
                        appeal_state_change=appeals_state_change,
                        answer_type=answer.answer_type,
                        comment=answer.comment,
                        reject_reason=answer.reject_reason.name
                        if answer.reject_reason
                        else None,
                    )
                )

        AppealAnswer.objects.bulk_create(answers_to_create)

    def update_categories(self):
        """Добавляет новые категории из ПОС, старым задает флаг deleted, если в ПОС они были удалены"""
        categories = self.pos_service.get_subjects()
        current_categories_ids = self._get_current_categories_pos_ids()
        categories_to_add: List[Category] = []

        for category in categories:
            if category.id not in current_categories_ids:
                new_category = self._create_category_entity(category)
                categories_to_add.append(new_category)

        new_categories = Category.objects.bulk_create(categories_to_add)
        deleted_categories = self._update_deleted_categories()
        updated_categories = new_categories + deleted_categories

        logger.info(
            f"updated categories ids: {list(map(lambda category: category.pk, updated_categories))}"
        )

    def update_subcategories(self):
        """Добавляет новые подкатегории из ПОС, старым задает флаг deleted, если в ПОС они были удалены"""
        subcategories = self._get_all_subcategories_entities_from_pos()
        current_subcategories_ids = self._get_current_subcategories_pos_ids()
        subcategories_to_add: List[Subcategory] = []

        for subcategory in subcategories:
            if subcategory.pos_id not in current_subcategories_ids:
                subcategories_to_add.append(subcategory)

        new_subcategories = Subcategory.objects.bulk_create(subcategories_to_add)
        deleted_subcategories = self._update_deleted_subcategories()
        updated_subcategories = new_subcategories + deleted_subcategories

        logger.info(
            f"updated subcategories ids: {list(map(lambda subcategory: subcategory.pk, updated_subcategories))}"
        )

    def update_appeals(self, appeals: Iterable[Appeal] = None):
        if not appeals:
            appeals = Appeal.objects.exclude(
                status__in=(AppealState.MODERATION_REJECTED, AppealState.RESPONDED)
            )
        for appeal in appeals:
            try:
                self._update_appeal(appeal)
            except:
                logger.error(f"fail update appeal, id: {appeal.pk}")

        logger.info(
            f"update appeals ids: {list(map(lambda appeal: appeal.pk, appeals))}"
        )
