from django.core.cache import cache
from django.db import models

KEY_PREFIX = "initiative_data"


def save_initiative_old_data(initiative, data):
    old_data = {}
    for attr, value in data.items():
        if isinstance(value, list):
            old_data[attr] = initiative.files.values_list("id", flat=True)
        elif isinstance(value, models.Model):
            model = getattr(initiative, attr, None)
            if model:
                old_data[attr] = model.id
        else:
            old_data[attr] = getattr(initiative, attr, None)
    cache.set(f"{KEY_PREFIX}_{initiative.pk}", old_data)


def restore_initiative_initial_data(initiative, serializer):
    data = cache.get(f"{KEY_PREFIX}_{initiative.pk}", None)
    if data:
        serializer = serializer(instance=initiative, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
