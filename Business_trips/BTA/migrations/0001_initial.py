# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 10:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=200)),
                ('office', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateField(blank=True, null=True)),
                ('finish_time', models.DateField(blank=True, null=True)),
                ('departure', models.CharField(blank=True, max_length=200)),
                ('arrival', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trips', to='BTA.City')),
            ],
        ),
    ]
