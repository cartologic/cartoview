from rest_framework import permissions, viewsets

from cartoview.layers.models import Layer

from ..permissions import IsOwnerOrReadOnly
from ..serializers.layers import LayerSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    filterset_fields = ('name', 'title', 'description',
                        'server__server_type', 'server__id',
                        'server__owner__username')
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
