from django.contrib import admin

from config.settings import settings
from .category import CategoryAdmin
from .file import FileAdmin
from .location import LocationAdmin
from .plan import PlanAdmin
from .plan_comment import PlanCommentAdmin
from .department_category import DepartmentCategoryAdmin


if settings.INVENTORY_STANDALONE:
    admin.site.unregister(category.Category)
    admin.site.unregister(file.File)
    admin.site.unregister(location.Location)
    admin.site.unregister(plan.Plan)
    admin.site.unregister(plan_comment.PlanComment)
    admin.site.unregister(department_category.DepartmentCategory)
