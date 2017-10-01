# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0004_auto_20171001_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='license',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
