# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import delft3dworker.models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('delft3dworker', '0080_auto_20161121_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='version',
            field=jsonfield.fields.JSONField(default=delft3dworker.models.version_default),
        ),
    ]