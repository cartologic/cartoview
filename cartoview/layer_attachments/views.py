import os
import shutil
import django_filters
from django.conf import settings
from django.http import HttpResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from geonode.layers.models import Layer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render

from .models import LayerAttachment
from .serializers import AttachmentSerializer, LayerSerializer
from ..app_manager.views import StandardAppViews
from .apps import LayerAttachmentsConfig


class LayerViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows layers to be viewed only
    """

    def get_queryset(self):
        """
        Override the default queryset to retrieve only the layers that have attachments
        """
        target_layer_ids = []
        for instance in Layer.objects.all():
            if instance.layer_attachments.all().count() > 0:
                target_layer_ids.append(instance.id)
        return Layer.objects.filter(id__in=target_layer_ids)

    serializer_class = LayerSerializer


class AttachmentFilter(django_filters.FilterSet):
    class Meta:
        model = LayerAttachment
        fields = ['id', 'layer__id', 'layer__typename', 'feature_id', 'created_by__username']


class AttachmentViewSet(ModelViewSet):
    """
    API endpoint that allows collection records attachments to be viewed or edited
    """
    queryset = LayerAttachment.objects.all()
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttachmentFilter

    def perform_create(self, serializer):
        layer_typename = self.request.POST.get('layer_typename')
        layer_feature_id = self.request.POST.get('layer_feature_id')
        layer = Layer.objects.filter(typename=layer_typename).first()
        return serializer.save(created_by=self.request.user, layer=layer, feature_id=layer_feature_id)


class DownloadAttachmentsView(APIView):

    def get(self, request, format=None):
        """
        Return a zipped file of all task attachments
        """
        layer_typename = request.GET.get('layer_typename', '')
        layer_feature_id = request.GET.get('layer_feature_id', '')
        target_dir = os.path.join(settings.MEDIA_ROOT, LayerAttachmentsConfig.name, 'attachments', layer_typename,
                                  layer_feature_id)
        result_file = shutil.make_archive(target_dir, 'zip', target_dir)
        if os.path.exists(result_file):
            with open(result_file, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/x-zip-compressed")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(result_file)
                return response
        raise Http404


class AttachmentManagerViews(StandardAppViews):
    """
    Standard app views add the necessary methods "add/edit/ etc..."
    """
    pass


def view(request):
    return render(request, 'attachment_manager/view.html')
