from django.template.loaders.app_directories import Loader as AppsLoader
import io
import os
from django.template.base import TemplateDoesNotExist


class Loader(AppsLoader):
    def load_template_source(self, template_name, template_dirs=None):
        from django.conf import settings
        apps_template_dirs = []
        if settings.APPS_DIR and os.path.isdir(settings.APPS_DIR):
            apps_template_dirs = [os.path.join(settings.APPS_DIR, name, 'templates') for name in os.listdir(
                settings.APPS_DIR) if os.path.isdir(os.path.join(settings.APPS_DIR, name, 'templates'))]
        for app_tmpl_dir in apps_template_dirs:
            filepath = os.path.join(app_tmpl_dir, template_name)
            if not os.path.isfile(filepath):
                continue
            try:
                with io.open(filepath, encoding=self.engine.file_charset) as fp:
                    return fp.read(), filepath
            except IOError:
                pass
        raise TemplateDoesNotExist(template_name)
