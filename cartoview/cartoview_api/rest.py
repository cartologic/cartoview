from django.core.urlresolvers import reverse
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from geonode.api.api import OwnersResource
from geonode.base.models import ResourceBase

type_filter = {
    'app': 'appinstance',
    'doc': 'document',
    'map': 'map',
    'layer': 'Layer'
}


class AllResourcesResource(ModelResource):
    type = fields.CharField(null=False, blank=False)
    app = fields.DictField(null=True, blank=False)
    urls = fields.DictField(null=False, blank=False)
    owner = fields.ToOneField(OwnersResource, 'owner', full=True)
    thumbnail_url = fields.CharField(null=True, blank=True)

    class Meta:
        resource_name = 'all_resources'
        queryset = ResourceBase.objects.distinct()
        fields = ['id', 'title', 'abstract',
                  'type', 'featured', 'owner__username']
        filtering = {
            'id': ALL,
            'title': ALL,
            'abstract': ALL,
            'featured': ALL,
            'owner': ALL_WITH_RELATIONS
        }
        limit = 100

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(AllResourcesResource, self).build_filters(filters)
        if('resource_type' in filters):
            resource_type = filters['resource_type']
            orm_filters.update({'resource_type': resource_type})

        return orm_filters

    def type_filter(self, filter, queryset):
        filter = filter.lower()
        result = []
        if filter in type_filter:
            for item in queryset:
                if hasattr(item, type_filter[filter]):
                    result.append(item)
                elif filter == 'layer' and \
                        not hasattr(item, type_filter['app']) and\
                        not hasattr(item, type_filter['doc']) and\
                        not hasattr(item, type_filter['map']):
                    result.append(item)
        else:
            result = queryset
        return result

    def dehydrate_thumbnail_url(self, bundle):
        thumb = bundle.obj.thumbnail_url
        if not thumb and hasattr(bundle.obj, 'appinstance') and\
                bundle.obj.appinstance.map:
            thumb = bundle.obj.appinstance.map.thumbnail_url
        return thumb

    def apply_filters(self, request, applicable_filters):
        resource_type = applicable_filters.pop('resource_type', None)
        filtered = super(AllResourcesResource, self).apply_filters(
            request, applicable_filters)
        if resource_type:
            filtered = self.type_filter(resource_type, filtered)
        return filtered

    def dehydrate_owner(self, bundle):
        return bundle.obj.owner.username

    def dehydrate_app(self, bundle):
        item = bundle.obj
        if hasattr(item, 'appinstance'):
            return {'name': item.appinstance.app.name,
                    'title': item.appinstance.app.title}
        else:
            return None

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
