# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0002_app_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='status',
            field=models.CharField(default='Alpha', max_length=100),
        ),
    ]
