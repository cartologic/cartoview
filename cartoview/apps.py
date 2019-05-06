from django.apps import AppConfig


class CartoviewAppConfig(AppConfig):
    name = "cartoview"
    verbose_name = "Cartoview"

    def ready(self):
        super(CartoviewAppConfig, self).ready()
        from django.conf import settings
        from .celery_app import app as celery_app
        if celery_app not in settings.INSTALLED_APPS:
            settings.INSTALLED_APPS += (celery_app, )
