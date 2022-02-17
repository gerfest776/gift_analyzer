import django_filters
from django_filters import rest_framework

from villagers.models import Villager


class VillagersFilter(rest_framework.FilterSet):
    """Filter for Villagers

    QueryParams:
        order_by - field which sorts by birth_date(order_by = <UUID>)
        town - field which sorts by citizen_towns(town = <UUID>)

    """

    order_by = django_filters.OrderingFilter(fields=["birth_date"])

    class Meta:
        model = Villager
        fields = ["town"]
