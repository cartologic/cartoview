from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from django.db.models import Q
from tastypie.resources import ModelResource
from myapp.models import Song


class SongResource(ModelResource):
    class Meta:
        queryset = Song.objects.all()
        resource_name = 'song'
        authentication = ApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True

        filtering = {
            'id': ['exact'],
            'rank': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
            'song': ['exact', 'icontains'],
            'artist': ['exact', 'icontains'],
        }

    def build_filters(self, filters=None, ignore_bad_filters=True):
        if filters is None:
            filters = {}

        orm_filters = super(SongResource, self).build_filters(filters)

        if('search' in filters):
            query = filters['search']
            qset = (
                    Q(artist__icontains=query) |
                    Q(song__icontains=query)
                    )
            orm_filters.update({'custom': qset})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(SongResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered

