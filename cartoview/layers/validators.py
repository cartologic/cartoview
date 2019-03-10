from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
pattern = re.compile(r'^EPSG:[\d]{0,26}')


def validate_projection(value):
    if not pattern.match(value):
        raise ValidationError(
            _('%(value)s is not a valid projection'),
            params={'value': value},
        )
