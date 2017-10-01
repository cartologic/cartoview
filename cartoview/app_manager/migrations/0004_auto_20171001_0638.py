# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0003_app_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='app',
            name='category',
        ),
        migrations.AlterField(
            model_name='app',
            name='license',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='app',
            name='category',
            field=models.ManyToManyField(related_name='apps', null=True, to='app_manager.AppType'),
        ),
    ]
