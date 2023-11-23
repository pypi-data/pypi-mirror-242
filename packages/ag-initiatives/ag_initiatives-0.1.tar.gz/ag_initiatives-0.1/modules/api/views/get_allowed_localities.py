from django.http import JsonResponse
from rest_framework.decorators import api_view

from ...core.models import Locality, Department


@api_view(["GET"])
def get_allowed_localities(request):
    selected_value = request.GET.get('selected_value', None)
    if selected_value:
        filtered_choices = Locality.objects.filter(departments__id=selected_value)
        choices = [{'id': item.id, 'name': item.name} for item in filtered_choices]
    else:
        choices = []

    return JsonResponse({'choices': choices})


@api_view(["GET"])
def get_allowed_categories(request):
    selected_value = request.GET.get('selected_value', None)
    if not selected_value:
        return JsonResponse({'choices': []})
    department = Department.objects.filter(id=selected_value).first()
    if not department:
        return JsonResponse({'choices': []})
    if not hasattr(department, 'sub_permissions'):
        return JsonResponse({'choices': []})
    sub_permissions = department.sub_permissions
    choices = {
        'voting_categories': list(sub_permissions.voting_categories.values('id', 'name')),
        'initiative_categories': list(sub_permissions.initiative_categories.values('id', 'name')),
        'map_works_categories': list(sub_permissions.map_works_categories.values('id', 'name')),
        'plans_categories': list(sub_permissions.plans_categories.values('id', 'name')),
        'appeals_categories': list(sub_permissions.appeals_categories.values('id', 'name')),
        'suggestion_categories': list(sub_permissions.suggestion_categories.values('id', 'name')),
        'encouragement_categories': list(sub_permissions.encouragement_categories.values('id', 'name')),
    }
    return JsonResponse({'choices': choices})
