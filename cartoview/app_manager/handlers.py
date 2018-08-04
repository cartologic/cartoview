import os
import sys

from django.utils.importlib import import_module
from django.core.urlresolvers import clear_url_caches
from django.template import context, base, loader
from django.utils import translation
from django.utils.translation import trans_real


def setup_django_settings(test_settings):
    """Override the enviroment variable and call the _setup method of the settings object to reload them."""
    os.environ['DJANGO_SETTINGS_MODULE'] = test_settings

    from django.conf import settings as django_settings

    if test_settings:
        # reload settings
        reload_settings(django_settings)
    else:
        # just settings cleanup, no reload
        django_settings._wrapped = None


def reload_settings(settings):
    """Special routine to reload django settings, including:
    urlconf module, context processor, templatetags settings, database settings.
    This also includes re-setting up sqlalchemy database settings. Environment chosen is always TestEnv."""

    # resetup django settings
    settings._setup()

    # check if there's settings to reload
    if hasattr(settings, 'ROOT_URLCONF'):
        if settings.ROOT_URLCONF in sys.modules:
            reload(sys.modules[settings.ROOT_URLCONF])
        import_module(settings.ROOT_URLCONF)
        settings.LANGUAGE_CODE = 'en'  # all tests should be run with English by default
        import django.core.cache
        django.core.cache.cache = django.core.cache.get_cache(
            django.core.cache.DEFAULT_CACHE_ALIAS)

        # clear django urls cache
        clear_url_caches()
        # clear django contextprocessors cache
        context._standard_context_processors = None
        # clear django templatetags cache
        base.templatetags_modules = None

        # reload translation files
        reload(translation)
        reload(trans_real)

        # clear django template loaders cache
        loader.template_source_loaders = None
        from django.template.loaders import app_directories
        reload(app_directories)
