from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from cartoview.layers.models import Layer
from rest_framework.filters import SearchFilter, OrderingFilter
from ..filters import DjangoObjectPermissionsFilter, LayerFilter
from ..serializers.layers import LayerSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    filterset_class = LayerFilter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoObjectPermissionsFilter,
                       DjangoFilterBackend, OrderingFilter, SearchFilter)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
