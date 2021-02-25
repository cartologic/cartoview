from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GeonodeAllauthProviderConfig(AppConfig):
    name = 'geonode_allauth_provider'
    verbose_name = _("GeoNode Allauth Provider")
