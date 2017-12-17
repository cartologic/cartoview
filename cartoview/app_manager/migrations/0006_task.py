# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_manager', '0005_delete_apptag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(default=0, choices=[(1, 'Periodic Task'), (0, 'A-Periodic Task')])),
                ('status', models.IntegerField(default=0, choices=[(1, 'FINISHED'), (0, 'In Progress')])),
                ('every', models.FloatField(default=0, null=True, blank=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('finished_at', models.DateTimeField(null=True)),
                ('result', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
