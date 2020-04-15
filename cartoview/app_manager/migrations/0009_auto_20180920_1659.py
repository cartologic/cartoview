# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('app_manager', '0008_appinstance_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='appstore',
            name='server_type',
            field=models.CharField(default='Geoserver', max_length=256,
                                   choices=[('Exchange', 'Exchange'), ('Geoserver', 'Geoserver'),
                                            ('QGISServer', 'QGISServer')]),
        ),
        migrations.AlterField(
            model_name='app',
            name='license',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
