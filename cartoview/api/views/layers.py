from rest_framework import permissions, viewsets

from cartoview.layers.models import Layer

from ..filters import DjangoObjectPermissionsFilter, LayerFilter
from ..serializers.layers import LayerSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    filterset_class = LayerFilter
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = (DjangoObjectPermissionsFilter,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
