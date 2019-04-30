import django_filters
from rest_framework.filters import BaseFilterBackend

from cartoview.app_manager.models import App, AppInstance
from cartoview.layers.models import Layer
from cartoview.maps.models import Map

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
    server = django_filters.CharFilter(
        lookup_expr='exact', field_name='server__id')

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


class DjangoObjectPermissionsFilter(BaseFilterBackend):
    """
    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """
    perm_format = '%(app_label)s.view_%(model_name)s'
    shortcut_kwargs = {
        'accept_global_perms': False,
    }

    def filter_queryset(self, request, queryset, view):
        # We want to defer this import until runtime, rather than import-time.
        # See https://github.com/encode/django-rest-framework/issues/4608
        # (Also see #1624 for why we need to make this import explicitly)
        from guardian.shortcuts import get_objects_for_user

        user = request.user
        permission = self.perm_format % {
            'app_label': queryset.model._meta.app_label,
            'model_name': queryset.model._meta.model_name,
        }

        return get_objects_for_user(
            user, permission, queryset,
            **self.shortcut_kwargs)
