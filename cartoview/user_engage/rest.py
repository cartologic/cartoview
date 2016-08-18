from cartoview.app_manager.resources import BaseModelResource, FileUploadResource
from tastypie.resources import Resource, ModelResource
from .models import *
from tastypie.constants import ALL_WITH_RELATIONS, ALL
from tastypie.authorization import Authorization
from tastypie import fields
from avatar.templatetags.avatar_tags import avatar_url
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest, UnsupportedFormat
from django.utils.encoding import force_text, smart_bytes
from django.utils import six
from PIL import Image as PILImage
from django.conf import settings
import os

class MultipartFormSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        self.content_types['file_upload'] = 'multipart/form-data'
        self.formats.append('file_upload')
        super(MultipartFormSerializer, self).__init__(*args, **kwargs)

    def from_file_upload(self, data, options=None):
        request = options['request']
        deserialized = {}
        for k in request.POST:
            deserialized[str(k)] = str(request.POST[k])
        for k in request.FILES:
            deserialized[str(k)] = request.FILES[k]
        return deserialized

    # add request param to extract files
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


class ImageResource(FileUploadResource):
    user = fields.DictField(readonly=True)
    thumbnail = fields.CharField(readonly=True)

    class Meta:
        serializer = MultipartFormSerializer()
        queryset = Image.objects.all()
        filtering = {"identifier": ALL}
        can_edit = True
        authorization = Authorization()

    def save(self, bundle, skip_errors=False):
        bundle.obj.user = bundle.request.user
        return super(ImageResource, self).save(bundle, skip_errors)


    def dehydrate_user(self, bundle):
        return dict(username=bundle.obj.user.username, avatar=avatar_url(bundle.obj.user, 60))

    def dehydrate_thumbnail(self, bundle):
        if bundle.obj.image is None or bool(bundle.obj.image) == False:
            return None
        size = bundle.request.GET.get('thumbnailSize', '80,80')
        THUMBNAIL_SIZE = [int(d) for d in size.split(",")]
        image_filename = os.path.basename(bundle.obj.image.file.name)
        thumbnail_dir_name = "%dx%d" % (THUMBNAIL_SIZE[0],THUMBNAIL_SIZE[1],)
        thumbnail_dir = os.path.join(settings.MEDIA_ROOT, 'user_engage' , 'images' ,'thumbnails', thumbnail_dir_name)
        thumbnail_filename = os.path.join(thumbnail_dir , image_filename)
        if not os.path.exists(thumbnail_filename):
            if not os.path.exists(thumbnail_dir):
                os.makedirs(thumbnail_dir)
            image = PILImage.open(bundle.obj.image.file)
            image.thumbnail(THUMBNAIL_SIZE, PILImage.ANTIALIAS)
            image.save(thumbnail_filename)
        return "%s/user_engage/images/thumbnails/%s/%s"  % (settings.MEDIA_URL, thumbnail_dir_name, image_filename)

class CommentResource(ModelResource):
    user = fields.DictField(readonly=True)

    class Meta:
        queryset = Comment.objects.all()
        filtering = {"identifier": ALL}
        can_edit = True
        authorization = Authorization()

    def save(self, bundle, skip_errors=False):
        bundle.obj.user = bundle.request.user
        return super(CommentResource, self).save(bundle, skip_errors)

    def dehydrate_user(self, bundle):
        return dict(username=bundle.obj.user.username, avatar=avatar_url(bundle.obj.user, 60))
