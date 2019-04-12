import random
from django import template

register = template.Library()


@register.simple_tag
def get_empty_image():
    number = random.randint(1, 8)
    return "material-kit/assets/img/bg" + str(number) + ".jpg"
