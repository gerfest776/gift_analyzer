from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from villagers.filters import VillagersFilter
from villagers.models import Importer, Villager
from villagers.pagination import Pagination
from villagers.serializers import (
    BirthdaySerializer,
    ImportSerializer,
    PartialSerializer,
    PercentileSerializer,
    UPCitizenSerializer,
)


class CreateVillagerView(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    serializer_class = ImportSerializer
    queryset = Importer.objects.all()
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    lookup_field = "import_id"

    def get_serializer_class(self):
        if self.action == "towns":
            return PercentileSerializer
        elif self.action == "citizens_birthdays":
            return BirthdaySerializer
        elif self.action == "citizens":
            return UPCitizenSerializer
        elif self.action == "citizen":
            return PartialSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        if self.action == "citizens":
            qs = Villager.objects.filter(importer_id=int(self.kwargs["import_id"]))
            self.filterset_class = VillagersFilter
            self.filter = self.filterset_class(self.request.GET, queryset=qs)
            return self.filter.qs
        else:
            return self.queryset

    @action(
        methods=["patch"],
        detail=True,
        url_path="citizen/(?P<citizen_id>[^/.]+)",
        url_name="citizens-patch",
    )
    def citizen(self, request, import_id, citizen_id):
        return self.partial_update(request)

    @action(
        methods=["get"],
        detail=False,
        url_path="citizens/(?P<import_id>[^/.]+)",
        url_name="citizens",
    )
    def citizens(self, request, import_id):
        return self.list(request)

    @action(
        methods=["get"],
        detail=True,
        url_path="citizens/birthdays",
        url_name="citizens-birthdays",
    )
    def citizens_birthdays(self, request, import_id):
        return self.retrieve(request)

    @action(
        methods=["get"],
        detail=True,
        url_path="towns/stat/percentile/age",
        url_name="citizens-percentile",
    )
    def towns(self, request, import_id):
        return self.retrieve(request)
