from rest_framework import serializers
from cartoview.layers.models import Layer
from cartoview.connections.utils import get_server_by_value


class LayerSerializer(serializers.ModelSerializer):
    server = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:servers-detail'
    )
    server_info = serializers.SerializerMethodField()
    layer_type = serializers.CharField(read_only=True)
    proxyable = serializers.BooleanField(read_only=True)
    owner = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    def get_server_info(self, obj):
        s = get_server_by_value(obj.server_type)
        data = {
            "type": s.title,
            "url": obj.server_url,
            "title": obj.server.title,
            "proxy": obj.server_proxy,
            "operations": obj.server_operations
        }
        return data

    class Meta:
        model = Layer
        fields = '__all__'
