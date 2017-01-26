# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0003_auto_20161123_1134'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(verbose_name=b'App Store URL')),
            ],
        ),
        migrations.AlterField(
            model_name='app',
            name='tags',
            field=models.ManyToManyField(to='app_manager.AppTag', blank=True),
        ),
    ]
