from django.db import models


# Create your models here.
class InstalledApps(models.Model):
    version = models.CharField(max_length=10)
    name = models.CharField(unique=True, max_length=50)


class AppStore(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(verbose_name="App Store URL")

    def __str__(self):
        return self.name
