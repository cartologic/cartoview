from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json

from django import template
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import mark_safe
from future import standard_library
from pinax.ratings.models import Rating

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
