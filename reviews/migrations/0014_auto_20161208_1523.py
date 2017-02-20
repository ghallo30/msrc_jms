# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_reviewdetails_date_invited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewdetails',
            name='date_ended',
            field=models.DateField(verbose_name='date ended', null=True),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='date_start',
            field=models.DateField(verbose_name='date started', null=True),
        ),
    ]
