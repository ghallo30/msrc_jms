# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0005_auto_20161206_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='policies',
            name='content_type',
            field=models.CharField(default='G', choices=[('G', 'Guidelines'), ('P', 'Policies')], max_length=2),
        ),
    ]
