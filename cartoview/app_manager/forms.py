# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.forms import FileField, ModelForm
from django.utils.translation import ugettext_lazy as _
# TODO: Review this file. Legacy??!
from future import standard_library
from geonode.base.forms import ResourceBaseForm
from modeltranslation.forms import TranslationModelForm

from .models import App, AppInstance

standard_library.install_aliases()


class AppInstallerForm(ModelForm):
    error_messages = {
        'duplicate_app_name':
            _("An application with the same user has already installed."),
        'invalid_package_file':
            _("The uploaded file is not an application package."),
    }
    package_file = FileField()

    class Meta(object):
        model = App
        fields = ("package_file",)


class AppForm(ModelForm):
    class Meta(object):
        model = App
        fields = ("title",)


class AppInstanceForm(TranslationModelForm):
    class Meta(object):
        model = AppInstance
        fields = [
            'title',
            'abstract',
        ]


class AppInstanceEditForm(ResourceBaseForm):
    class Meta(ResourceBaseForm.Meta):
        model = AppInstance
        exclude = ResourceBaseForm.Meta.exclude
