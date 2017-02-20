# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0009_auto_20161130_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlefile',
            name='open_access',
            field=models.BooleanField(default=False),
        ),
    ]
