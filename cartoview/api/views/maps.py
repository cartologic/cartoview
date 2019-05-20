from cartoview.log_handler import get_logger
from cartoview.maps.models import Map
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from ..filters import MapFilter
from ..permissions import IsOwnerOrReadOnly
from ..serializers.layers import LayerSerializer
from ..serializers.maps import MapSerializer

logger = get_logger(__name__)


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all().prefetch_related('layers').distinct()
    serializer_class = MapSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_class = MapFilter

    @action(detail=True, methods=['get'], url_name='map_config')
    def map_config(self, request, pk=None):
        try:
            map_obj = Map.objects.get(pk=pk)
        except ObjectDoesNotExist as e:
            raise NotFound(str(e))
        layers = [LayerSerializer(lyr,
                                  context={'request': request}).data
                  for lyr in map_obj.layers.all()]
        render_options = map_obj.render_options
        if 'ordering' in render_options.keys():
            sorted_layers = {}
            for l in layers:
                layer_id = l['id']
                try:
                    ordering = render_options['ordering']
                    index = ordering[str(layer_id)]
                    sorted_layers[index] = l
                except KeyError as e:
                    logger.error(e)
                    sorted_layers[layer_id] = l
            layers = [sorted_layers[i] for i in sorted(sorted_layers.keys())]
        serializer = MapSerializer(map_obj)
        data = serializer.data
        data.update({'layers': layers})
        return Response(data, status=200)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
