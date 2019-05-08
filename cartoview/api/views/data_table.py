from rest_framework import viewsets
from cartoview.data_table.models import DataTable
from cartoview.api.serializers.data_table import DataTableSerializer


class DataTableViewSet(viewsets.ModelViewSet):
    queryset = DataTable.objects.all()
    serializer_class = DataTableSerializer
