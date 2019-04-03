from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from cartoview.maps.models import Map

from ..permissions import IsOwnerOrReadOnly
from ..serializers.layers import LayerSerializer
from ..serializers.maps import MapSerializer
from ..filters import MapFilter


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all().prefetch_related('layers')
    serializer_class = MapSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_class = MapFilter

    @action(detail=True, methods=['get'], url_name='map_json')
    def map_json(self, request, pk=None):
        try:
            map_obj = Map.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            raise NotFound(str(e))
        layers = [LayerSerializer(lyr,
                                  context={'request': request}).data
                  for lyr in map_obj.layers.all()]
        serializer = MapSerializer(map_obj)
        data = serializer.data
        data.update({'layers': layers})
        return Response(data, status=200)
