from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppInstancesCatalogConfig(AppConfig):
    name = 'app_instances_catalog'
    verbose_name = _("CartoView App Instances")
