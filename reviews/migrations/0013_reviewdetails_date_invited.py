# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0012_auto_20161208_0650'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewdetails',
            name='date_invited',
            field=models.DateTimeField(null=True, verbose_name='date invited'),
        ),
    ]
