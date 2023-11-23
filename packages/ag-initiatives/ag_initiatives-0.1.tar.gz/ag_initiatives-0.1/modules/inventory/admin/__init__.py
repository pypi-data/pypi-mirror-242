from .admin_site import inventory_admin_site
from .passport import PassportAdmin, Passport
from .passport_summary import PassportSummaryAdmin, PassportSummary


inventory_admin_site.register(Passport, PassportAdmin)
inventory_admin_site.register(PassportSummary, PassportSummaryAdmin)
