from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible


@deconstructible
class ListValidator(object):
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def validate_field(self, value):
        if self.min_length and value:
            if len(value) < self.min_length:
                raise ValidationError(
                    _('%(value)s has invalid min length it should be %(min_length)s'),
                    params={'value': value, 'min_length': self.min_length},
                )
        if self.max_length and value:
            if len(value) > self.max_length:
                raise ValidationError(
                    _('%(value)s has invalid max length it should be %(max_length)s'),
                    params={'value': value, 'max_length': self.max_length},
                )

    def __call__(self, value):
        self.validate_field(value)
