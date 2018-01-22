from geonode.base.models import ResourceBase
from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from django.core.urlresolvers import reverse


class AllResoucesResource(ModelResource):
    type = fields.CharField(null=False, blank=False)
    urls = fields.DictField(null=False, blank=False)

    class Meta:
        queryset = ResourceBase.objects.distinct()
        fields = ['id', 'title', 'abstract',
                  'thumbnail_url', 'type', 'featured']
        filtering = {
            'id': ALL,
            'title': ALL,
            'abstract': ALL,
            'featured': ALL
        }

    def dehydrate_urls(self, bundle):
        item = bundle.obj
        urls = dict(details=item.detail_url)
        if hasattr(item, 'appinstance'):
            urls["view"] = reverse('%s.view' % item.appinstance.app.name,
                                   args=[str(item.appinstance.id)])
        elif hasattr(item, 'document'):
            urls["download"] = reverse(
                'document_download', None, [str(item.id)])
        elif hasattr(item, 'map'):
            urls["view"] = reverse('map_view', None, [str(item.id)])
        return urls

    def dehydrate_type(self, bundle):
        item = bundle.obj
        if hasattr(item, 'appinstance'):
            return "App"
        elif hasattr(item, 'document'):
            return "Doc"
        elif hasattr(item, 'map'):
            return "Map"
        else:
            return "Layer"
