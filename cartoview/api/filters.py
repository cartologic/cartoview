from cartoview.maps.models import Map
from cartoview.layers.models import Layer
from cartoview.app_manager.models import App, AppInstance
import django_filters
BASE_FILTER_FIELDS = {
    "title": ["exact", "iexact", "contains", "icontains", "in",
              "startswith", "istartswith", "endswith", "iendswith"],
    "description": ["exact", "iexact", "contains", "icontains", "in",
                    "startswith", "istartswith", "endswith",
                    "iendswith"],
    "created_at": ["exact", "iexact", "contains", "icontains", "in",
                   "startswith", "istartswith", "endswith",
                   "iendswith"],
    "updated_at": ["exact", "iexact", "contains", "icontains", "gt", "gte",
                   "lt", "lte"], }


class BaseFilter(django_filters.FilterSet):
    owner = django_filters.CharFilter(
        lookup_expr='iexact', field_name='owner__username')


class MapFilter(BaseFilter):

    class Meta:
        model = Map
        fields = BASE_FILTER_FIELDS


class LayerFilter(BaseFilter):

    class Meta:
        model = Layer
        fields = BASE_FILTER_FIELDS


class AppFilter(django_filters.FilterSet):
    class Meta:
        model = App
        fields = BASE_FILTER_FIELDS


class AppInstanceFilter(BaseFilter):

    class Meta:
        model = AppInstance
        fields = BASE_FILTER_FIELDS
