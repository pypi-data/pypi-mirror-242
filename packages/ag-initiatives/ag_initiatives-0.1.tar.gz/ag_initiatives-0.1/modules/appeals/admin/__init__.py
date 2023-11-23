# from django.contrib import admin
#
# from config.settings import settings
# from .appeal import AppealAdmin
# from .category import CategoryAdmin
# from .reject_reason import RejectReasonAdmin
# from .contractor import ContractorAdmin
# from .department_category import DepartmentCategoryAdmin
#
#
# if settings.DEBUG:
#     from .file import File
#
# if settings.INVENTORY_STANDALONE:
#     admin.site.unregister(appeal.Appeal)
#     admin.site.unregister(category.Category)
#     admin.site.unregister(reject_reason.RejectReason)
#     admin.site.unregister(contractor.Contractor)
#     admin.site.unregister(department_category.DepartmentCategory)
#     if settings.DEBUG:
#         admin.site.unregister(file.File)
