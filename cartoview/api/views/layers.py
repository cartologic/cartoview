from rest_framework import viewsets

from cartoview.layers.models import Layer

from ..serializers.layers import LayerSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    filterset_fields = ('name', 'title', 'description',
                        'server__server_type')
    # permissions_classes = (permissions.IsAdminUser,)
