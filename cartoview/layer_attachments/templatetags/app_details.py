from django import template
from ..apps import LayerAttachmentsConfig

register = template.Library()


# app version
@register.simple_tag
def app_version():
    return LayerAttachmentsConfig.version
