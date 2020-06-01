from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf.urls import url
from django.db import models
from django.forms.models import modelform_factory
from django.shortcuts import render
from future import standard_library
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from .serializers import HTMLSerializer, MultipartFormSerializer

standard_library.install_aliases()


class BaseMeta(object):
    object_class = None
    always_return_data = True
    serializer = HTMLSerializer()
    authorization = Authorization()


class BaseModelResource(ModelResource):
    class Meta(BaseMeta):
        pass

    def build_schema(self):
        base_schema = super(BaseModelResource, self).build_schema()
        for f in self._meta.object_class._meta.fields:
            if f.name in base_schema['fields'] and f.choices:
                base_schema['fields'][f.name].update({
                    'choices': f.choices,
                })
        return base_schema

    def get_form(self, obj=None):
        form = modelform_factory(self._meta.object_class)
        return form(instance=obj)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/edit/(?P<pk>.*?)/$" %
                self._meta.resource_name, self.wrap_view('edit')),
            url(r"^(?P<resource_name>%s)/new/$" % self._meta.resource_name,
                self.wrap_view('new_item'))
        ]

    def new_item(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        form = self.get_form()
        return render(request, 'app_manager/rest_api/edit.html', {
            'form': form,
            'operation': 'add',
            'resource_uri': self.get_resource_uri()
        })

    def edit(self, request, pk, **kwargs):
        self.method_check(request, allowed=['get'])
        obj = self._meta.object_class.objects.get(id=pk)
        form = self.get_form(obj)
        return render(request, 'app_manager/rest_api/edit.html', {
            'form': form,
            'operation': 'edit',
            'resource_uri': self.get_resource_uri()
        })


class FileUploadResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        object_class = None
        serializer = MultipartFormSerializer()

    def obj_create(self, bundle, **kwargs):
        bundle = super(FileUploadResource, self).obj_create(bundle, **kwargs)
        for f in bundle.obj._meta.fields:
            if isinstance(f, models.FileField):
                file = bundle.request.FILES.get(f.name, None)
                if file:
                    f.save_form_data(bundle.obj, file)
        return bundle

    def deserialize(self, request, data, format='application/json'):
        deserialized = self._meta.serializer.deserialize(
            data,
            request=request,
            format=request.META.get('CONTENT_TYPE', 'application/json'))
        return deserialized
