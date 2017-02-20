# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_articlefile_open_access'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='articlefile',
            name='version_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
