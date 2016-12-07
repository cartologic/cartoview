# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(verbose_name=b'App Store URL')),
            ],
        ),
    ]
