# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0006_auto_20170108_0308'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='store',
            field=models.ForeignKey(to='app_manager.AppStore', null=True),
        ),
    ]
