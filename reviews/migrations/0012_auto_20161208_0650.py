# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0011_auto_20161207_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewdetails',
            name='cancelled',
        ),
        migrations.RemoveField(
            model_name='reviewdetails',
            name='replaced',
        ),
        migrations.AddField(
            model_name='assigneditor',
            name='date_cancelled',
            field=models.DateTimeField(verbose_name='date cancelled', null=True),
        ),
        migrations.AddField(
            model_name='assigneditor',
            name='date_replaced',
            field=models.DateTimeField(verbose_name='date replaced', null=True),
        ),
        migrations.AddField(
            model_name='assigneditor',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='date_cancelled',
            field=models.DateTimeField(verbose_name='date cancelled', null=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='date_replaced',
            field=models.DateTimeField(verbose_name='date replaced', null=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
