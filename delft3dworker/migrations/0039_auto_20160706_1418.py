# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('delft3dworker', '0038_searchform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchform',
            name='sections',
            field=jsonfield.fields.JSONField(default=b'[]'),
        ),
    ]
