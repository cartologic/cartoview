from rest_framework import serializers
from cartoview.data_table.models import DataTable


class DataTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataTable
        fields = ('name', 'values')
