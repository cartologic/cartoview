# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
# TODO: Review this file. Legacy??!
from future import standard_library
standard_library.install_aliases()
from builtins import *
from builtins import object
from django.forms import FileField, ModelForm
from django.utils.translation import ugettext_lazy as _
from geonode.base.forms import ResourceBaseForm
from .models import App, AppInstance
from modeltranslation.forms import TranslationModelForm


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
