from django.contrib import admin
from django.db import connections, models


class DynamicModel(object):
    @classmethod
    def create_model(cls, name, table_name, fields=None, app_label='',
                     module='', options=None, admin_opts=None):
        options = {
            'db_table': table_name,
        }

        class Meta:
            # Using type('Meta', ...) gives a dictproxy error during model creation
            pass

        if app_label:
            # app_label must be set using the Meta inner class
            setattr(Meta, 'app_label', app_label)

        # Update Meta with any options that were provided
        if options is not None:
            for key, value in options.items():
                setattr(Meta, key, value)

        # Set up a dictionary to simulate declarations within a class
        attrs = {'__module__': module, 'Meta': Meta}

        # Add in any fields that were provided
        if fields:
            attrs.update(fields)

        model = type(name, (models.Model,), attrs)

        # Create an Admin class if admin options were provided
        if admin_opts is not None:
            class Admin(admin.ModelAdmin):
                pass

            for key, value in admin_opts:
                setattr(Admin, key, value)
            admin.site.register(model, Admin)

        return model

    @classmethod
    def create_model_table(cls, model, connection=None):
        if not connection:
            connection = cls.get_connection_by_name()
        with connection.schema_editor() as editor:
            editor.create_model(model)

    @classmethod
    def delete_model_table(cls, model, connection=None):
        if not connection:
            connection = cls.get_connection_by_name()
        with connection.schema_editor() as editor:
            editor.delete_model(model)

    @classmethod
    def get_connection_by_name(cls, name='default'):
        dc = None
        for conn in connections.all():
            if conn.alias == name:
                dc = conn
        if not dc:
            raise Exception("Connection with name: {} not found!".format(name))
        return dc

    @classmethod
    def check_table_exists(cls, table_name, connection=None):
        if not connection:
            connection = cls.get_connection_by_name()
        return (table_name in connection.introspection.table_names())
