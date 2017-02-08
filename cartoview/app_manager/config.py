import yaml
import os
from django.conf import settings


class Item(yaml.YAMLObject):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    # __getattr__ is called if the object doesn't have the attribute as member
    # this to avoid "object has no attribute" error and make the object acts like javascript
    def __getattr__(self, name):
        return None


class Collection(object):
    def __init__(self, file_path=None, items=None):
        self._items = []
        if items is None:
            items = []
        for item in items:
            self.append(item)
        self.yaml_file_path = file_path
        if self.yaml_file_path is not None:
            self.load()
        self.default_sort()

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __len__(self):
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __delitem__(self, item):
        self._items.remove(item)


    def default_sort(self):
        return self

    def append(self, item):
        self._items.append(item)

    def _load(self, yaml_file):
        all_items = yaml.load(yaml_file)
        if all_items is None:
            return self
        for item in all_items:
            self.append(Item(**item))
        self.default_sort()
        return self

    def load(self):
        if os.path.exists(self.yaml_file_path):
            with open(self.yaml_file_path, 'r') as f:
                return self._load(f)
        return self


    def _save(self, yaml_file):
        yaml.dump([item.__dict__ for item in self._items], yaml_file, default_flow_style=False)


    def save(self):
        self.default_sort()
        with open(self.yaml_file_path, 'w') as f:
            self._save(f)


class App(Item):
    def __init__(self, **kwargs):
        super(App, self).__init__(**kwargs)
        self.name = str(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name


class AppsConfig(Collection):
    def __init__(self, file_path=None, items=None):
        if file_path is None:
            from django.conf import settings
            file_path = os.path.join(settings.APPS_DIR, "apps.yml")
        self._hash = {}
        super(AppsConfig, self).__init__(file_path, items)

    def append(self, item):
        if item.order is None:
            item.order = 0
        else:
            item.order = int(item.order)
        super(AppsConfig, self).append(item)
        self._hash[item.name] = item

    def get_by_name(self, name):
        return self._hash.get(name, None)

    def default_sort(self):
        self._items = sorted(self._items, key=lambda c: c.order)
        return self

    def __delitem__(self, item):
        super(AppsConfig, self).__delitem__(item)
        del self._hash[item.name]