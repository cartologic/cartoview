import ast
import json

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import ValidationError as RestValidationError


class ListField(models.TextField):
    description = _("List Field")

    def _parse_from_db(self, value):
        if isinstance(value, str):
            value = ast.literal_eval(value)
        if not isinstance(value, list):
            raise ValidationError(_("Invalid data for a List"))
        return value

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self._parse_from_db(value)

    def to_python(self, value):
        if value is None or isinstance(value, list):
            return value
        return self._parse_from_db(value)

    def get_prep_value(self, value):
        if isinstance(value, tuple):
            value = list(value)
        if not isinstance(value, list):
            raise ValidationError(
                _("{} is not a an instance list".format(value)))
        return json.dumps(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.to_python(value)


class ListSerializerField(serializers.Field):

    def to_representation(self, value):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return json.loads(value)
        return value

    def to_internal_value(self, data):
        if not isinstance(data, list):
            raise RestValidationError(_("List Type Is Required"))
        return data


class DictField(models.TextField):
    description = _("Dict Field")

    def _eval_data(self, data):
        return ast.literal_eval(data)

    def _parse_from_db(self, value):
        if not isinstance(value, str):
            raise ValidationError(_("Invalid data for Dict Field"))
        return json.loads(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self._parse_from_db(value)

    def to_python(self, value):
        try:
            value = self._eval_data(value)
        except BaseException:
            raise ValidationError(_("Invalid data for Dict Field"))
        if value is None or isinstance(value, dict):
            return value
        return self._parse_from_db(value)

    def get_prep_value(self, value):
        if not isinstance(value, str):
            return json.dumps(value)
        return value

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.to_python(value)
