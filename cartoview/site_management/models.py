from django.db import models
from django.contrib.sites.models import Site
from datetime import datetime

# Create your models here.


def get_site_logo_path(instance, filename):
    today = datetime.now()
    date_as_path = today.strftime("%Y/%m/%d")
    return '/'.join(['site_logos', date_as_path, filename])


class SiteLogo(models.Model):
    site = models.OneToOneField(Site)
    logo = models.ImageField(upload_to=get_site_logo_path)

    def __unicode__(self):
        return "Logo: {}".format(self.logo.url)
