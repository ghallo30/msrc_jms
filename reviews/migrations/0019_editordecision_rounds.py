# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_auto_20161214_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='editordecision',
            name='rounds',
            field=models.IntegerField(default=1),
        ),
    ]
