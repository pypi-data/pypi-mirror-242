from django.contrib import admin

from config.settings import settings
from .contractor import ContractorAdmin
from .institution_type import InstitutionTypeAdmin
from .work_category import WorkCategoryAdmin
from .work_reason import WorkReasonAdmin
from .work_type import WorkTypeAdmin
from .works import WorksAdmin
from .department_category import DepartmentCategoryAdmin


if settings.INVENTORY_STANDALONE:
    admin.site.unregister(contractor.Contractor)
    admin.site.unregister(institution_type.InstitutionType)
    admin.site.unregister(work_category.WorkCategory)
    admin.site.unregister(work_reason.WorkReason)
    admin.site.unregister(work_type.WorkType)
    admin.site.unregister(works.Works)
    admin.site.unregister(department_category.DepartmentCategory)
