from rest_framework import permissions, viewsets

from cartoview.layers.models import Layer

from ..permissions import BaseObjectPermissions
from ..serializers.layers import LayerSerializer
from ..filters import LayerFilter


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    # filterset_fields = ('name', 'title', 'description',
    #                     'server__server_type', 'server__id',
    #                     'server__owner__username')
    filterset_class = LayerFilter
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, BaseObjectPermissions)
