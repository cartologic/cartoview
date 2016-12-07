import json
from itertools import chain
from django import template
register = template.Library()
from ..signals import widgets
from django.utils.safestring import mark_safe

# @register.assignment_tag(takes_context=True)
# def viewer_widgets(context):
#     all_widgets = [w for func, w in widgets.send(sender='get_viewer_widgets')]
#     return list(chain.from_iterable(all_widgets))


@register.filter()
def dump_json(obj):
    # if obj is None:
    #     return "null"
    return mark_safe(json.dumps(obj))