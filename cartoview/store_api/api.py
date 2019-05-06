# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import Resource


class GenericApiResource(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class StoreAppVersion(Resource):
    id = fields.IntegerField()
    app = fields.CharField()
    build_no = fields.IntegerField()
    cartoview_version = fields.ListField()
    changelog = fields.CharField()
    logo = fields.CharField()
    installation_instructions = fields.CharField()
    download_link = fields.CharField()
    created_at = fields.DateTimeField()
    modified_at = fields.DateTimeField()
    dependencies = fields.DictField()
    downloads = fields.IntegerField()
    resource_uri = fields.CharField()
    version = fields.CharField()

    class Meta:
        resource_name = 'store_app_version'
        object_class = GenericApiResource

    def obj_get(self, bundle, **kwargs):
        data = bundle.data
        obj = GenericApiResource(initial=data)
        return obj


class StoreAppResource(Resource):
    id = fields.IntegerField()
    approved = fields.BooleanField()
    rejected = fields.BooleanField()
    author = fields.CharField()
    author_website = fields.CharField()
    created_at = fields.DateTimeField()
    demo_url = fields.CharField()
    description = fields.CharField()
    title = fields.CharField()
    status = fields.CharField()
    tags = fields.ListField()
    type = fields.ListField()
    downloads = fields.IntegerField()
    stars = fields.IntegerField()
    license = fields.DictField()
    latest_version = fields.ForeignKey(StoreAppVersion, 'latest_version')
    modified_at = fields.DateTimeField()
    name = fields.CharField()
    resource_uri = fields.CharField()
    server_type = fields.DictField()
    single_instance = fields.BooleanField()

    class Meta:
        resource_name = 'store_app'
        object_class = GenericApiResource

    def obj_get(self, bundle, **kwargs):
        data = bundle.data
        latest_version = data.pop('latest_version', None)
        obj = GenericApiResource(initial=data)
        api_obj = StoreAppVersion()
        if latest_version:
            bundle = api_obj.build_bundle(data=latest_version)
            v_obj = api_obj.obj_get(bundle)
            obj.latest_version = v_obj
        return obj
