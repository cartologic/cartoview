import json
from itertools import chain
from django import template
register = template.Library()
from django.utils.safestring import mark_safe


@register.filter()
def dump_json(obj):
    # if obj is None:
    #     return "null"
    return mark_safe(json.dumps(obj))