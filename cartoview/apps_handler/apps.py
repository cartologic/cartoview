from django.apps import AppConfig
from django.conf import settings
import yaml
import os
from django.core.management import call_command


class AppsHandlerConfig(AppConfig):
    name = 'cartoview.apps_handler'
    verbose_name = "Apps Handler"

    def execute_pending(self):
        #TODO: fix racing
        pending_yaml = settings.PENDING_APPS
        if os.path.exists(pending_yaml):
            with open(pending_yaml, 'r') as f:
                pending_apps = yaml.load(f) or []
                for app in pending_apps:
                    call_command("makemigrations", app, interactive=False)
                    try:
                        call_command("migrate", app, interactive=False)
                    except:
                        pass
            with open(pending_yaml, 'w+') as f:
                yaml.dump([], f)
        else:
            pass

    def ready(self):
        self.execute_pending()
