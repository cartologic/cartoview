from django import forms
from modeltranslation.forms import TranslationModelForm
from geonode.base.forms import ResourceBaseForm

__author__ = 'Amr'

from django.forms import ModelForm, FileField
from models import *
from django.utils.translation import ugettext, ugettext_lazy as _


class AppInstallerForm(ModelForm):
    error_messages = {
        'duplicate_app_name': _("An application with the same user has already installed."),
        'invalid_package_file': _("The uploaded file is not an application package."),
    }
    package_file = FileField()

    class Meta:
        model = App
        fields = ("package_file",)


class AppForm(ModelForm):
    class Meta:
        model = App
        fields = ("title",)


class AppInstanceForm(TranslationModelForm):
    class Meta:
        model = AppInstance
        fields = ['title', 'abstract',]


class AppInstanceEditForm(ResourceBaseForm):
    class Meta(ResourceBaseForm.Meta):
        model = AppInstance
        exclude = ResourceBaseForm.Meta.exclude



