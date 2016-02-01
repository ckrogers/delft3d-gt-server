# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelRuns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('uuid', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=256)),
                ('progress', models.IntegerField()),
                ('timeleft', models.IntegerField()),
            ],
        ),
    ]
