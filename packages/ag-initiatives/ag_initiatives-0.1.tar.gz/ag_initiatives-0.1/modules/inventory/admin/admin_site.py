from django.contrib.admin import AdminSite


class InventoryAdminSite(AdminSite):
    site_header = "Инвентаризация общественных территорий Красноярского края"
    site_title = "Инвентаризация общественных территорий Красноярского края"
    index_title = "Инвентаризация общественных территорий Красноярского края"


inventory_admin_site = InventoryAdminSite(name="inventory_admin")
