from ast import parse

from cartoview.connections.utils import get_module_class
from django.core.exceptions import ValidationError
from django.db import models

from .factory import DynamicModel

# NOTE: Hey!! You don't blame me for this, The Following Shit is just a requirement


def field_name_validator(value):
    try:
        parse('{} = None'.format(value))
    except (SyntaxError, ValueError, TypeError):
        raise ValidationError("{} is not valid field name".format(value))


class Model(models.Model):
    name = models.CharField(max_length=255, validators=[
        field_name_validator, ], null=False, blank=False, unique=True)
    created = models.BooleanField(default=False, null=False, blank=False)
    @property
    def model_class(self):
        module_name = 'fake_project.{}.no_models'.format(self.name.lower())
        return DynamicModel.create_model(self.name.capitalize(), self.name, app_label='fake_app',
                                         module=module_name,
                                         fields=self.model_fields)

    def create_table(self):
        if not DynamicModel.check_table_exists(self.name):
            DynamicModel.create_model_table(self.model_class)
            self.created = True
            self.save()

    def delete_table(self):
        if DynamicModel.check_table_exists(self.name):
            DynamicModel.delete_model_table(self.model_class)
            self.created = False
            self.save()

    @property
    def model_fields(self):
        fields = {}
        for field in self.fields.all():
            module_name, class_name = get_module_class(field.field_type)
            mod = __import__(module_name, fromlist=[class_name, ])
            field_class = getattr(mod, class_name)
            fields.update({field.name: field_class(null=True, blank=True)})
        return fields

    def __str__(self):
        return self.name


class ModelField(models.Model):
    TEXT_FIELD = "django.db.models.TextField"
    NUMBER_FIELD = "django.db.models.FloatField"
    FIELD_CHOICES = (
        (TEXT_FIELD, 'Text'),
        (NUMBER_FIELD, 'Number'),
    )
    field_type = models.TextField(choices=FIELD_CHOICES, null=False, blank=False)
    name = models.CharField(max_length=255, validators=[
        field_name_validator, ], null=False, blank=False)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='fields')

    def __str__(self):
        return self.name
