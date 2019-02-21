import json

from django import template
from django.utils.html import mark_safe

register = template.Library()


@register.filter()
def jsonify(obj):
    return mark_safe(json.dumps(obj))
