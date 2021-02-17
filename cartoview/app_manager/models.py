from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from datetime import datetime

from cartoview.app_manager.config import CartoviewApp
from cartoview.log_handler import get_logger
from django.conf import settings as geonode_settings
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from future import standard_library

from jsonfield import JSONField
from taggit.managers import TaggableManager

logger = get_logger(__name__)

standard_library.install_aliases()


class AppTypeManager(models.Manager):
    def without_apps_duplication(self):
        return super(AppTypeManager, self).get_queryset().distinct('apps')


@python_2_unicode_compatible
class AppType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    objects = AppTypeManager()

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AppStore(models.Model):
    """
    to store links for cartoview appstores
    """
    SERVER_CHOICES = (
        ('Exchange', 'Exchange'),
        ('Geoserver', 'Geoserver'),
        ('QGISServer', 'QGISServer'),
    )
    name = models.CharField(max_length=256)
    url = models.URLField(verbose_name="App Store URL")
    is_default = models.BooleanField(default=False)
    server_type = models.CharField(
        max_length=256, choices=SERVER_CHOICES, default="Geoserver")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class App(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    app_url = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    author_website = models.URLField(null=True, blank=True)
    license = models.CharField(max_length=200, null=True, blank=True)
    tags = TaggableManager()
    date_installed = models.DateTimeField(
        'Date Installed', auto_now_add=True, null=True)
    installed_by = models.ForeignKey(
        geonode_settings.AUTH_USER_MODEL, null=True,
        blank=True, on_delete=models.PROTECT)
    single_instance = models.BooleanField(
        default=False, null=False, blank=False)
    category = models.ManyToManyField(AppType, related_name='apps')
    status = models.CharField(
        max_length=100, blank=False, null=False, default='Alpha')
    owner_url = models.URLField(null=True, blank=True)
    help_url = models.URLField(null=True, blank=True)
    app_img_url = models.TextField(max_length=1000, blank=True, null=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    version = models.CharField(max_length=10)
    store = models.ForeignKey(AppStore, null=True, on_delete=models.PROTECT)
    order = models.IntegerField(null=True, default=0)

    default_config = JSONField(default={})

    class meta(object):
        ordering = ['order']

    def __str__(self):
        return self.title

    @property
    def settings_url(self):
        try:
            return reverse("%s_settings" % self.name)
        except BaseException as e:
            logger.error(e)
            return None

    @property
    def urls(self):
        admin_urls = logged_in_urls = anonymous_urls = None
        try:
            app_module = __import__(self.name)
            if hasattr(app_module, 'urls_dict'):
                urls_dict = getattr(app_module, 'urls_dict')
                if 'admin' in list(urls_dict.keys()):
                    admin_urls = urls_dict['admin']
                else:
                    admin_urls = None
                if 'logged_in' in list(urls_dict.keys()):
                    logged_in_urls = urls_dict['logged_in']
                else:
                    logged_in_urls = None
                if 'anonymous' in list(urls_dict.keys()):
                    anonymous_urls = urls_dict['anonymous']
                else:
                    anonymous_urls = None
        except ImportError as e:
            logger.error(e)
        return (admin_urls, logged_in_urls, anonymous_urls)

    @property
    def open_url(self):
        from django.urls import reverse
        open_url = reverse('app_manager_base_url') + self.name
        try:
            app_module = __import__(self.name)
            if hasattr(app_module, 'OPEN_URL_NAME'):
                open_url = reverse(getattr(app_module, 'OPEN_URL_NAME'))
        except ImportError as e:
            logger.error(e)
        return open_url

    @property
    def create_new_url(self):
        from django.urls import reverse
        create_new_url = reverse('{}.new'.format(self.name))
        try:
            app_module = __import__(self.name)
            if hasattr(app_module, 'CREATE_NEW_URL_NAME'):
                create_new_url = reverse(
                    getattr(app_module, 'CREATE_NEW_URL_NAME'))
        except ImportError as e:
            logger.error(e)
        return create_new_url

    @property
    def admin_urls(self):
        return self.urls[0]

    @property
    def logged_in_urls(self):
        return self.urls[1]

    @property
    def anonymous_urls(self):
        return self.urls[2]

    @property
    def new_url(self):
        try:
            return reverse("%s.new" % self.name)
        except BaseException as e:
            logger.error(e)
            return None

    def set_active(self, active=True):
        app = CartoviewApp.objects.get(self.name, None)
        if app:
            app.active = active
            app.commit()
            CartoviewApp.save()
        return app

    @property
    def config(self):
        return CartoviewApp.objects.get(self.name, None)


def get_app_logo_path(instance, filename):
    today = datetime.now()
    date_as_path = today.strftime("%Y/%m/%d")
    return '/'.join([
        'app_instance_logos',
        slugify(instance.title), date_as_path, filename
    ])
