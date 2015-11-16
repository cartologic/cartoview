import time
import json
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer
from django.template.loader import render_to_string
from tastypie.exceptions import BadRequest, UnsupportedFormat
from django.utils import six
from django.utils.encoding import force_text, smart_bytes


class HTMLSerializer(Serializer):
    def to_html(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        json_data = json.dumps(data, cls=json.JSONEncoder, indent=4, sort_keys=True)
        return render_to_string('app_manager/rest_api/base.html', {'json_data': json_data})





class MultipartFormSerializer(HTMLSerializer):
    def __init__(self, *args, **kwargs):
        self.content_types['file_upload'] = 'multipart/form-data'
        self.formats.append('file_upload')
        super(type(self), self).__init__(*args, **kwargs)

    def from_file_upload(self, data, options=None):
        request = options['request']
        deserialized = {}
        for k in request.POST:
            deserialized[str(k)] = str(request.POST[k])
        #for k in request.FILES:
        #    deserialized[str(k)] = request.FILES[k]
        return deserialized

    #add request param to extract files
    def deserialize(self, content, request= None, format='application/json'):
        """
        Given some data and a format, calls the correct method to deserialize
        the data and returns the result.
        """
        desired_format = None

        format = format.split(';')[0]

        for short_format, long_format in self.content_types.items():
            if format == long_format:
                if hasattr(self, "from_%s" % short_format):
                    desired_format = short_format
                    break

        if desired_format is None:
            raise UnsupportedFormat("The format indicated '%s' had no available deserialization method. Please check your ``formats`` and ``content_types`` on your Serializer." % format)

        if isinstance(content, six.binary_type) and desired_format != 'file_upload':
            content = force_text(content)

        deserialized = getattr(self, "from_%s" % desired_format)(content, {'request': request})
        return deserialized