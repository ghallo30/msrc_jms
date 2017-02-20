# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0019_editordecision_rounds'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigneditor',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
