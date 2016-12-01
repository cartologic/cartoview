# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0002_auto_20161120_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='date_installed',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'Date Installed', null=True),
        ),
    ]
