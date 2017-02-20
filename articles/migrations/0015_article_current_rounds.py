# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0014_auto_20161214_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='current_rounds',
            field=models.IntegerField(default=1),
        ),
    ]
