from django import template

register = template.Library()


@register.simple_tag
def cartoview_version():
    return __import__('cartoview').__version__
