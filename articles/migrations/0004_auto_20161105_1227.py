# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20161105_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='references',
            field=models.TextField(null=True),
        ),
    ]
