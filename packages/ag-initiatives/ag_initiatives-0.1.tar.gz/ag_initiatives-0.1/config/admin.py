from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    site_header = "Активный гражданин"
    site_title = "Активный гражданин"

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request, app_label)
        app_list = sorted(app_dict.values(), key=self.sorting_function)
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        return app_list

    @staticmethod
    def sorting_function(app_dict: dict):
        if app_dict["name"].split('.')[0].isdigit():
            return int(app_dict["name"].split('.')[0]), app_dict.values
        return 100, app_dict["name"].lower()


custom_admin_site = CustomAdminSite(name="admin")
