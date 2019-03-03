# -*- coding: utf-8 -*-


class GenericObject:
    def __init__(self, **data):
        self._data = data
        for k, v in data.items():
            if isinstance(v, dict):
                self.__dict__[k] = GenericObject(**v)
            else:
                self.__dict__[k] = v

    def get_attributes(self):
        attrs = vars(self)
        attrs.pop('_data', None)
        return attrs


def serialize_json(data):
    return GenericObject(**data)
