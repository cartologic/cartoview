# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0006_app_default_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logo',
            name='site',
        ),
        migrations.AlterField(
            model_name='app',
            name='category',
            field=models.ManyToManyField(related_name='apps',
                                         to='app_manager.AppType'),
        ),
        migrations.DeleteModel(
            name='Logo',
        ),
    ]
