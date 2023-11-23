from django.apps import apps


def get_plug_in_modules():
    plug_in_apps = [
        (item.name.replace("modules.", ""), item.verbose_name)
        for item in apps.get_app_configs()
        if hasattr(item, "plug_in") and item.plug_in
    ]
    return plug_in_apps
