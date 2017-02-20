# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0007_auto_20161222_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='jmsmessage',
            name='is_task',
            field=models.BooleanField(default=False),
        ),
    ]
