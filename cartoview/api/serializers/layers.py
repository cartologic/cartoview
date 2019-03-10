from rest_framework import serializers
from cartoview.layers.models import Layer
from cartoview.connections.models import Server


class ServerTypeField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]


class LayerSerializer(serializers.ModelSerializer):
    server = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='api:servers-detail'
    )
    server_type = ServerTypeField(read_only=True, choices=Server.SERVER_TYPES)
    server_url = serializers.CharField(read_only=True)

    class Meta:
        model = Layer
        fields = '__all__'
