from django.contrib import admin
from import_export.admin import ImportMixin
from import_export.fields import Field
from import_export.formats.base_formats import XLSX
from import_export.resources import ModelResource

from modules.appeals_pos.models.category import Category
from modules.appeals_pos.models.subcategory import Subcategory


def update_or_create_subcategory(category_id: int, sub_id: int, sub_name: str):
    """Создание подкатегории категории по данным из xlsx файла"""
    if sub_qs := Subcategory.objects.filter(pos_id=sub_id):
        sub_qs.update(category=category_id, name=sub_name, deleted=False)
    else:
        Subcategory.objects.create(
            category_id=category_id,
            pos_id=sub_id,
            name=sub_name,
            deleted=False,
        )


class CategoryResource(ModelResource):
    pos_id = Field(attribute="pos_id", column_name="ID Категории")
    name = Field(attribute="name", column_name="Категория")

    class Meta:
        model = Category
        exclude = ("id", "image", "icon", "color", "deleted", "fact_id", "fact")
        import_id_fields = ('pos_id',)
        store_instance = True

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        """Всем категориям, которые отсутствуют в файле, устанавливается статус УДАЛЕНА"""
        self._meta.model.objects.update(deleted=True)
        Subcategory.objects.update(deleted=True)

    def after_import_row(self, row, row_result, row_number=None, **kwargs):
        """Создание объектов подкатегорий"""
        try:
            update_or_create_subcategory(row_result.object_id, row["ID Подкатегории"], row["Подкатегория"])
        except (ValueError, AttributeError, TypeError):
            ...

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.deleted = False


@admin.register(Category)
class CategoryAdmin(ImportMixin, admin.ModelAdmin):
    formats = [XLSX]
    resource_class = CategoryResource
    list_display = ["id", "pos_id", "name", "is_available", "fact_id", "fact"]
    fields = ["pos_id", "name", "color", "image", "icon", "fact_id", "fact", "is_available"]
    readonly_fields = ["pos_id", "name", "fact_id", "fact", "is_available"]
    list_filter = ["deleted"]
    search_fields = ["pos_id", "name"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def is_available(self, instance):
        return not instance.deleted

    is_available.boolean = True
    is_available.short_description = "Доступно"

    class Meta:
        model = Category
