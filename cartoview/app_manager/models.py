import os
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
# from sorl.thumbnail.fields import ImageField
from apps_helper import delete_installed_app
from django.conf import settings as geonode_settings
from django.db.models import signals

# Create your models here.
from geonode.base.models import ResourceBase, resourcebase_post_save
from geonode.security.models import remove_object_permissions


class AppTag(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def __unicode__(self):
        return self.name


class App(models.Model):
    def only_filename(instance, filename):
        return filename

    name = models.CharField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    app_url = models.URLField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)
    author_website = models.URLField(null=True, blank=True)
    license = models.CharField(max_length=200, null=True, blank=True)
    tags = models.ManyToManyField(AppTag, null=True, blank=True)
    date_installed = models.DateTimeField('Date Installed', auto_now_add=True)
    installed_by = models.ForeignKey(geonode_settings.AUTH_USER_MODEL, null=True, blank=True)
    single_instance = models.BooleanField(default=False, null=False, blank=False)
    order = models.SmallIntegerField(null=False, blank=False, default=0)
    owner_url = models.URLField(null=True, blank=True)
    help_url = models.URLField(null=True, blank=True)
    # app_logo = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True, null = True)
    is_suspended = models.NullBooleanField(null=True, blank=True, default=False)
    app_img_url = models.TextField(max_length=1000)
    in_menu = models.NullBooleanField(null=True, blank=True, default=True)
    admin_only = models.NullBooleanField(null=True, blank=True, default=False)
    rating = models.IntegerField(default=0, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    def delete(self):
        delete_installed_app(self)
        super(type(self), self).delete()

    def __unicode__(self):
        return self.title


class AppInstance(ResourceBase):
    """
    An App Instance  is any kind of App Instance that can be created out of one of the Installed Apps.
    """

    # Relation to the App model
    app = models.ForeignKey(App, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('appinstance_detail', args=(self.id,))

    @property
    def name_long(self):
        if not self.title:
            return str(self.id)
        else:
            return '%s (%s)' % (self.title, self.id)

def pre_save_appinstance(instance, sender, **kwargs):
    if instance.abstract == '' or instance.abstract is None:
        instance.abstract = 'No abstract provided'

    if instance.title == '' or instance.title is None:
        instance.title = 'No title provided'





def pre_delete_appinstance(instance, sender, **kwargs):
    remove_object_permissions(instance.get_self_resource())

def create_thumbnail(sender, instance, created, **kwargs):
    from geonode.base.models import Link

    if not instance.has_thumbnail():
        parent_app_thumbnail_url = App.objects.get(id=instance.app.pk).app_img_url
        Link.objects.get_or_create(resource=instance,
                                   url=parent_app_thumbnail_url,
                                   defaults=dict(
                                       name='Thumbnail',
                                       extension='png',
                                       mime='image/png',
                                       link_type='image',
                                   ))

        instance.thumbnail_url=parent_app_thumbnail_url
        instance.save()



signals.pre_save.connect(pre_save_appinstance, sender=AppInstance)
signals.post_save.connect(create_thumbnail, sender=AppInstance)

signals.post_save.connect(resourcebase_post_save, sender=AppInstance)
signals.pre_delete.connect(pre_delete_appinstance, sender=AppInstance)
