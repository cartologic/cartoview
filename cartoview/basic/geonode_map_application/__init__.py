APP_NAME = "geonode_map_application"

NEW_INSTANCE_URL_NAME = "%s.new_instance" % APP_NAME
EDIT_INSTANCE_URL_NAME = "%s.new_instance" % APP_NAME
INSTANCE_DETAILS_URL_NAME = "appinstance_detail" # from cartoview.app_manager.urls

NEW_INSTANCE_TPL = '%s/new_instance.html' % APP_NAME

# create context variable to be used in all views
shared_context = {}
for key, value in locals().items():
    if isinstance(value, basestring) and not key.startswith("_"):
        shared_context[key] = value
