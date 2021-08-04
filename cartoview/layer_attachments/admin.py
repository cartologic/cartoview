import os
from django.contrib import admin

from .models import LayerAttachment


class LayerAttachmentAdmin(admin.ModelAdmin):
    list_display = ('get_layer_name', 'get_file_name', 'get_file_size')

    def get_layer_name(self, obj):
        return obj.layer.name
    get_layer_name.short_description = 'Layer name'

    def get_file_name(self, obj):
        return os.path.basename(obj.file.name)
    get_file_name.short_description = 'File name'

    def get_file_size(self, obj):
        suffix = 'B'
        size = obj.file.size
        for unit in ['', 'K', 'M', 'G', 'T']:
            if abs(size) < 1024.0:
                return "%3.1f %s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f %s%s" % (size, 'Y', suffix)
    get_file_size.short_description = 'File size'


admin.site.register(LayerAttachment, LayerAttachmentAdmin)
