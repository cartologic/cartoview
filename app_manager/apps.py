from django.apps import AppConfig


class AppManagerConfig(AppConfig):
    name = 'app_manager'

    def ready(self):
        from .os_utils import create_apps_dir
        create_apps_dir()
        from .apps_operations import pending_handler
        pending_handler.execute_pending()
