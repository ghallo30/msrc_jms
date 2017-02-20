# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20161121_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdetails',
            name='cancelled',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='date_reminded',
            field=models.DateTimeField(verbose_name='date reminded', null=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]
