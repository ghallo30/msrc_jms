# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20161201_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdetails',
            name='is_invited',
            field=models.BooleanField(default=False),
        ),
    ]
