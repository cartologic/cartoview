# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0002_auto_20170207_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='order',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
