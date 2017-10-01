# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='category',
            field=models.CharField(default='Others', max_length=100),
        ),
    ]
