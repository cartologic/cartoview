from rest_framework import viewsets

from cartoview.layers.models import Layer

from ..serializers.layers import LayerSerializer


class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer
    # permissions_classes = (permissions.IsAdminUser,)
