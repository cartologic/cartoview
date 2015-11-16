from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import   Group
from django.contrib.sites.models import Site
from django.db.models.signals import post_save ,m2m_changed
from django.dispatch import receiver
#from sorl.thumbnail.fields import ImageField
from apps_helper import delete_installed_app
from django.conf import settings as geonode_settings

# Create your models here.
from geonode.base.models import ResourceBase


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
    #app_logo = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True, null = True)
    is_suspended = models.NullBooleanField(null=True, blank=True , default= False)
    #app_img = ImageField(upload_to=only_filename, help_text="The site will resize this master image as necessary for page display", blank=True, null = True)
    in_menu = models.NullBooleanField(null=True, blank=True , default= True)
    admin_only = models.NullBooleanField(null=True, blank=True , default= False)
    rating = models.IntegerField(default=0, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.EmailField (null=True, blank=True)

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
    app = models.ForeignKey(App ,null=True,blank=True)