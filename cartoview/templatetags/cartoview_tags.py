from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

from pinax.ratings.models import Rating
from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models import Count
from django.utils.html import mark_safe
from future import standard_library
from geonode.documents.models import Document
from geonode.groups.models import GroupProfile
from geonode.layers.models import Layer
from geonode.maps.models import Map
from guardian.shortcuts import get_objects_for_user

from cartoview.app_manager.models import App, AppInstance

standard_library.install_aliases()
register = template.Library()


@register.filter()
def dump_json(obj):
    # if obj is None:
    #     return "null"
    return mark_safe(json.dumps(obj))


@register.simple_tag
def num_ratings(obj):
    ct = ContentType.objects.get_for_model(obj)
    return len(Rating.objects.filter(object_id=obj.pk, content_type=ct))


@register.simple_tag(takes_context=True)
def facets(context):
    request = context['request']
    title_filter = request.GET.get('title__icontains', '')

    facet_type = context['facet_type'] if 'facet_type' in context else 'all'

    if not settings.SKIP_PERMS_FILTER:
        authorized = get_objects_for_user(
            request.user, 'base.view_resourcebase').values('id')

    if facet_type == 'documents':

        documents = Document.objects.filter(title__icontains=title_filter)

        if settings.RESOURCE_PUBLISHING:
            documents = documents.filter(is_published=True)

        if not settings.SKIP_PERMS_FILTER:
            documents = documents.filter(id__in=authorized)

        counts = documents.values('doc_type').annotate(count=Count('doc_type'))
        facets = dict([(count['doc_type'], count['count'])
                       for count in counts])

        return facets

    elif facet_type == 'appinstances':
        appinstances = AppInstance.objects.filter(
            title__icontains=title_filter)
        if settings.RESOURCE_PUBLISHING:
            appinstances = appinstances.filter(is_published=True)

        if not settings.SKIP_PERMS_FILTER:
            appinstances = appinstances.filter(id__in=authorized)

        counts = appinstances.values('app__title').annotate(
            count=Count('app__name'))
        facets = dict([(count['app__title'], count['count'])
                       for count in counts])
        return facets

    else:

        layers = Layer.objects.filter(title__icontains=title_filter)

        if settings.RESOURCE_PUBLISHING:
            layers = layers.filter(is_published=True)

        if not settings.SKIP_PERMS_FILTER:
            layers = layers.filter(id__in=authorized)

        counts = layers.values('storeType').annotate(count=Count('storeType'))
        count_dict = dict([(count['storeType'], count['count'])
                           for count in counts])

        facets = {
            'raster': count_dict.get('coverageStore', 0),
            'vector': count_dict.get('dataStore', 0),
            'remote': count_dict.get('remoteStore', 0),
        }

        # Break early if only_layers is set.
        if facet_type == 'layers':
            return facets

        maps = Map.objects.filter(title__icontains=title_filter)
        documents = Document.objects.filter(title__icontains=title_filter)

        if not settings.SKIP_PERMS_FILTER:
            maps = maps.filter(id__in=authorized)
            documents = documents.filter(id__in=authorized)

        facets['map'] = maps.count()
        facets['document'] = documents.count()
        if facet_type == 'home':
            facets['user'] = get_user_model().objects.exclude(
                username='AnonymousUser').count()
            facets['app'] = App.objects.count()
            facets['group'] = GroupProfile.objects.exclude(
                access="private").count()

            facets['layer'] = facets['raster'] + \
            facets['vector'] + facets['remote']

    return facets


@register.filter(name='objects_count')
def objects_count(instances, user):
    permitted = [instance for instance in instances if user.has_perm(
        'view_resourcebase', instance.get_self_resource())]
    return len(permitted)


@register.simple_tag(name='cartoview_reverse')
def reverse_url(url_name, *args, **kwargs):
    url = None
    try:
        url = reverse(url_name, args=args, kwargs=kwargs)
    except BaseException:
        pass
    return json.dumps(url)
