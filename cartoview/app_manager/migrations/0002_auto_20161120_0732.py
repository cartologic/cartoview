# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='app_img_url',
            field=models.TextField(max_length=1000, null=True, blank=True),
        ),
    ]
