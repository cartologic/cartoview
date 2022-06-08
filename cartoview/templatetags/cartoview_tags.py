from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

from pinax.ratings.models import Rating
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db.models import Count, Q
from django.utils.html import mark_safe
from future import standard_library

from geonode.base.models import HierarchicalKeyword
from guardian.shortcuts import get_objects_for_user

from geonode.base.templatetags.base_tags import facets as gn_facets

from cartoview.app_manager.models import AppInstance
from geonode.security.utils import get_visible_resources

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
    keywords_filter = request.GET.getlist('keywords__slug__in', None)
    owner_filter = request.GET.getlist('owner__username__in', None)
    date_gte_filter = request.GET.get('date__gte', None)
    date_lte_filter = request.GET.get('date__lte', None)
    date_range_filter = request.GET.get('date__range', None)

    facet_type = context.get('facet_type', 'all')

    if not settings.SKIP_PERMS_FILTER:
        authorized = []
        try:
            authorized = get_objects_for_user(
                request.user, 'base.view_resourcebase').values('id')
        except Exception:
            pass

    if facet_type == 'appinstances':
        appinstances = AppInstance.objects.filter(title__icontains=title_filter)
        if owner_filter:
            appinstances = appinstances.filter(owner__username__in=owner_filter)
        if date_gte_filter:
            appinstances = appinstances.filter(date__gte=date_gte_filter)
        if date_lte_filter:
            appinstances = appinstances.filter(date__lte=date_lte_filter)
        if date_range_filter:
            appinstances = appinstances.filter(date__range=date_range_filter.split(','))

        appinstances = get_visible_resources(
            appinstances,
            request.user if request else None,
            admin_approval_required=settings.ADMIN_MODERATE_UPLOADS,
            unpublished_not_visible=settings.RESOURCE_PUBLISHING,
            private_groups_not_visibile=settings.GROUP_PRIVATE_RESOURCES)

        if keywords_filter:
            treeqs = HierarchicalKeyword.objects.none()
            for keyword in keywords_filter:
                try:
                    kws = HierarchicalKeyword.objects.filter(name__iexact=keyword)
                    for kw in kws:
                        treeqs = treeqs | HierarchicalKeyword.get_tree(kw)
                except Exception:
                    # Ignore keywords not actually used?
                    pass

            appinstances = appinstances.filter(Q(keywords__in=treeqs))

        if not settings.SKIP_PERMS_FILTER:
            appinstances = appinstances.filter(id__in=authorized)

        counts = appinstances.values('subtype').annotate(count=Count('subtype'))
        facets = {count['subtype']: count['count'] for count in counts}

        return facets
    else:
        return gn_facets(context)


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
