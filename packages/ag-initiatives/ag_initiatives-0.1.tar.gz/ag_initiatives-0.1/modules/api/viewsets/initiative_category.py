from django.db.models import Q
from rest_framework import viewsets, permissions, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from modules.api.serializers import (
    InitiativeAcceptingSettingsShortSerializer,
    InitiativeCategoryTreeSerializer,
    InitiativeCategorySerializer,
)
from modules.core.models import User
from modules.initiatives.models import (
    InitiativeCategory,
    InitiativeAcceptingSettings,
    Initiative,
)


class InitiativeCategoryAPI(viewsets.ReadOnlyModelViewSet):
    queryset = InitiativeCategory.objects.all()
    serializer_class = InitiativeCategorySerializer

    def list(self, request, *args, **kwargs):
        return Response(
            InitiativeCategoryTreeSerializer(
                InitiativeCategory.objects.filter(parent__isnull=True), many=True
            ).data
        )

    @action(
        methods=["get"], detail=False, permission_classes=[permissions.IsAuthenticated]
    )
    def available(self, request):
        user: User = request.user
        user_locality = user.get_locality_for_initiative()

        # TODO settings.user_locality_check
        qs = InitiativeCategory.objects.filter(
            Q(initiative_accepting_settings__active=True) &
            Q(
                Q(initiative_accepting_settings__locality__parent=user_locality) |
                Q(initiative_accepting_settings__locality=user_locality) |
                Q(initiative_accepting_settings__locality__localities=user_locality)
            )
        ).distinct()
        res = {}

        def rec(category: InitiativeCategory):
            res[category.pk] = {
                "id": category.pk,
                "name": category.name,
                "color": category.color,
                "image": serializers.ImageField().to_representation(category.image),
                "children": [],
                "parent": category.parent.pk if category.parent else None,
            }
            if category.parent is None:
                return
            rec(category.parent)

        for category in qs:
            rec(category)

        res = [v for v in res.values()]

        def build_tree(raw_nodes):
            nodes = {}
            for i in raw_nodes:
                id, obj = (i["id"], i)
                nodes[id] = obj

            forest = []
            for i in raw_nodes:
                id, parent_id, obj = (i["id"], i["parent"], i)
                node = nodes[id]

                if parent_id is None:
                    forest.append(node)
                else:
                    parent = nodes[parent_id]
                    if "children" not in parent:
                        parent["children"] = []
                    parent["children"].append(node)

            return forest

        return Response(build_tree(res))

    @action(
        methods=["get"], detail=True, permission_classes=[permissions.IsAuthenticated]
    )
    def params(self, request, pk=None):
        user: User = request.user
        instance: InitiativeCategory = self.get_object()
        initiative_id = request.GET.get("initiative", None)
        initiative = Initiative.objects.filter(id=initiative_id).first()
        locality = []
        if hasattr(initiative, "locality"):
            locality = initiative.locality.all()
        try:
            s = InitiativeAcceptingSettings.objects.get(
                active=True,
                category=instance,
                locality__in=locality if locality
                else [user.get_locality_for_initiative()],
            )
        except Exception as e:
            raise ValidationError(
                "settings for for provided category locality not found"
            )

        return Response(InitiativeAcceptingSettingsShortSerializer(s).data)
