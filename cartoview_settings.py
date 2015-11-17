from settings import *
CARTOVIEW_ROOT =os.path.join( os.path.abspath(os.path.dirname(os.path.dirname(__file__))) , 'cartoview')
STATICFILES_DIRS.extend([os.path.join(CARTOVIEW_ROOT, "static")])

INSTALLED_APPS += ('cartoview.app_manager',)

if 'cartoview.app_manager' in INSTALLED_APPS:
    #auto load apps
    from cartoview.app_manager.apps_helper import get_apps_names, APPS_DIR

    CARTOVIEW_APPS = ()

    import importlib, sys

    for app_name in get_apps_names():
        try:
            CARTOVIEW_APPS += ('cartoview.apps.' + app_name,)
            #settings_module = importlib.import_module('apps.%s.settings' % app_name)
            app_settings_file = os.path.join(APPS_DIR, app_name, 'settings.py')
            if os.path.exists(app_settings_file):
                # By doing this instead of import, app/settings.py can refer to
                # local variables from settings.py without circular imports.
                execfile(app_settings_file)
                # CARTOVIEW2_APPS += settings_module.apps
                # this_module = sys.modules[__name__]
                # GLOBAL_SETTINGS = getattr(settings_module,'GLOBAL_SETTINGS',{})
                # for key in GLOBAL_SETTINGS:
                #     current_val = getattr(this_module,key,None)
                #     if current_val is None:
                #         setattr(this_module, key, GLOBAL_SETTINGS[key])
                #     else:
                #         print '==========================='
                #         print 'warning: app %s trying to set the settings item "%s" which already has a value.' % (app_name,key)
        except:
            pass

    INSTALLED_APPS += CARTOVIEW_APPS