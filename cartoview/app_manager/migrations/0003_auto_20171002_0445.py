# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0002_auto_20171001_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='tags',
            field=models.ManyToManyField(
                to='app_manager.AppTag',
                null=True,
                blank=True),
        ),
    ]
