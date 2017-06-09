# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-09 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BTA', '0009_auto_20170609_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='attendees',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='meeting',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='meeting',
            name='event_id',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='meeting',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
