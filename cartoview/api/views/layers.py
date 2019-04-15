from rest_framework import permissions, viewsets

from cartoview.layers.models import Layer

from ..permissions import BaseObjectPermissions
from ..serializers.layers import LayerSerializer
from ..filters import LayerFilter


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    filterset_class = LayerFilter
    permission_classes = (BaseObjectPermissions,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
