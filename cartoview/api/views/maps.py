from rest_framework import viewsets

from cartoview.maps.models import Map
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializers.maps import MapSerializer
from ..serializers.layers import LayerSerializer
import json


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    @action(detail=True, methods=['get'], url_name='map_json')
    def map_json(self, request, pk=None):
        map_obj = Map.objects.get(pk=pk)
        layers = [LayerSerializer(lyr,
                                  context={'request': request}).data
                  for lyr in map_obj.layers.all()]
        serializer = MapSerializer(map_obj)
        data = serializer.data
        center = data['center']
        data.update({'layers': layers, 'center': json.loads(center)})
        return Response(data, status=200)
