# -*- coding: utf-8 -*-
import json
import os
from collections import Mapping
import portalocker


class AppsDict(Mapping):
    def __init__(self, *args, **kw):
        self._app_data = dict(*args, **kw)

    def __setitem__(self, key, item):
        self._app_data[key] = item
        self.__sort_apps()

    def __getitem__(self, key):
        return self._app_data[key]

    def __repr__(self):
        return repr(self._app_data)

    def __len__(self):
        return len(self._app_data)

    def __delitem__(self, key):
        del self._app_data[key]

    def clear(self):
        return self._app_data.clear()

    def copy(self):
        return self._app_data.copy()

    def has_key(self, k):
        return k in self._app_data

    def update(self, *args, **kwargs):
        self._app_data.update(*args, **kwargs)
        self.__sort_apps()

    def keys(self):
        return self._app_data.keys()

    def values(self):
        return self._app_data.values()

    def items(self):
        return self._app_data.items()

    def pop(self, *args):
        return self._app_data.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self._app_data, dict_)

    def __contains__(self, item):
        return item in self._app_data

    def __iter__(self):
        return iter(self._app_data)

    def __unicode__(self):
        return str(repr(self._app_data))

    def __sort_apps(self):
        self._app_data = dict(
            sorted(self._app_data.items(), key=lambda item: item[1].order))

    def to_json(self):
        data = {k: v.to_dict() for k, v in self._app_data.items()}
        return json.dumps(data, indent=4, sort_keys=True)

    def from_json(self, data):
        def cartoview_app_dict(name, data):
            d = {'name': name}
            d.update(data)
            return d

        try:
            apps = json.loads(data)
            self._app_data = {
                k: CartoviewApp(cartoview_app_dict(k, v))
                for k, v in apps.items()
            }
            self.__sort_apps()
            return self._app_data
        except BaseException:
            return AppsDict()

    def get_active_apps(self):
        return {k: v for k, v in self._app_data.items() if v.active}

    def get_pending_apps(self):
        return {k: v for k, v in self._app_data.items() if v.pending}

    def app_exists(self, app_name):
        return self._app_data.get(app_name, None)


class CartoviewApp(object):
    app_attrs = frozenset(['name', 'active', 'pending', 'order'])
    objects = AppsDict()
    apps_dir = None

    def __init__(self, data):
        if not data and isinstance(data, dict):
            raise ValueError("data must be dict type")
        for k, v in data.items():
            setattr(self, k, v)
        self._validate()
        self.cleanup()
        self.commit()

    def _validate(self):
        for attr in CartoviewApp.app_attrs:
            if not hasattr(self, attr):
                raise ValueError('attr {} not found'.format(attr))

    def cleanup(self):
        for attr in vars(self).keys():
            if attr not in [
                'objects', 'app_attrs'
            ] and attr not in CartoviewApp.app_attrs and (
                    not attr.startswith('_') and not attr.startswith('_')):
                delattr(self, attr)

    def __setattr__(self, name, value):
        if name == ['objects', 'app_attrs']:
            raise ValueError("{} should be altered using classname")
        if name not in CartoviewApp.app_attrs:
            raise AttributeError("attribute '{}' not found ".format(name))
        super(CartoviewApp, self).__setattr__(name, value)

    def to_dict(self):
        return {
            k: getattr(self, k)
            for k in CartoviewApp.app_attrs if k != 'name'
        }

    @classmethod
    def get_apps_json_path(cls):
        return os.path.join(cls.apps_dir, 'apps.json')

    def commit(self):
        CartoviewApp.objects.update({self.name: self})
        return self

    @classmethod
    def load(cls):
        if os.path.exists(cls.get_apps_json_path()):
            with portalocker.Lock(
                    cls.get_apps_json_path(), 'r',
                    portalocker.LOCK_EX) as jf:
                data = jf.read()
                CartoviewApp.objects.from_json(data)

    @classmethod
    def save(cls):
        with portalocker.Lock(
                cls.get_apps_json_path(), 'w',
                portalocker.LOCK_EX) as jf:
            data = CartoviewApp.objects.to_json()
            jf.write(data)
