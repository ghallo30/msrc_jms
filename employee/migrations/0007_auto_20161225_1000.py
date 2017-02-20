# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20161225_0810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinterest',
            name='keyword',
        ),
        migrations.AddField(
            model_name='userinterest',
            name='interest',
            field=models.ForeignKey(to='employee.Category', null=True),
        ),
    ]
