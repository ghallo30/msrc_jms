# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_auto_20161208_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdetails',
            name='acceptability',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
