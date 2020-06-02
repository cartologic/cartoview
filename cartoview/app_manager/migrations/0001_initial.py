# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '24_initial'),
        ('base', '24_to_26'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(
                    max_length=200, null=True, blank=True)),
                ('title', models.CharField(
                    max_length=200, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('short_description', models.TextField(null=True, blank=True)),
                ('app_url', models.URLField(null=True, blank=True)),
                ('author', models.CharField(
                    max_length=200, null=True, blank=True)),
                ('author_website', models.URLField(null=True, blank=True)),
                ('license', models.CharField(
                    max_length=200, null=True, blank=True)),
                ('date_installed', models.DateTimeField(
                    auto_now_add=True,
                    verbose_name=b'Date Installed',
                    null=True)),
                ('single_instance', models.BooleanField(default=False)),
                ('owner_url', models.URLField(null=True, blank=True)),
                ('help_url', models.URLField(null=True, blank=True)),
                ('app_img_url', models.TextField(
                    max_length=1000, null=True, blank=True)),
                ('rating', models.IntegerField(
                    default=0, null=True, blank=True)),
                ('contact_name', models.CharField(
                    max_length=200, null=True, blank=True)),
                ('contact_email', models.EmailField(
                    max_length=254, null=True, blank=True)),
                ('version', models.CharField(max_length=10)),
                ('order', models.IntegerField(default=0, null=True)),
                ('installed_by', models.ForeignKey(
                    blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)),
            ], ),
        migrations.CreateModel(
            name='AppInstance',
            fields=[
                ('resourcebase_ptr', models.OneToOneField(
                    parent_link=True,
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    to='base.ResourceBase', on_delete=models.CASCADE)),
                ('config', models.TextField(null=True, blank=True)),
                ('app', models.ForeignKey(
                    blank=True, to='app_manager.App', null=True, on_delete=models.CASCADE)),
                ('map', models.ForeignKey(blank=True, to='maps.Map',
                                          null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
            bases=('base.resourcebase',), ),
        migrations.CreateModel(
            name='AppStore',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(verbose_name=b'App Store URL')),
                ('is_default', models.BooleanField(default=False)),
            ], ),
        migrations.CreateModel(
            name='AppTag',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('name', models.CharField(
                    max_length=200, unique=True, null=True, blank=True)),
            ], ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(
                    verbose_name='ID',
                    serialize=False,
                    auto_created=True,
                    primary_key=True)),
                ('logo', models.ImageField(upload_to=b'')),
                ('site', models.OneToOneField(to='sites.Site', on_delete=models.CASCADE)),
            ], ),
        migrations.AddField(
            model_name='app',
            name='store',
            field=models.ForeignKey(to='app_manager.AppStore', null=True, on_delete=models.CASCADE), ),
        migrations.AddField(
            model_name='app',
            name='tags',
            field=models.ManyToManyField(to='app_manager.AppTag',
                                         blank=True), ),
    ]
