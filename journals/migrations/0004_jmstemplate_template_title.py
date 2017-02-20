# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0003_auto_20161108_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='jmstemplate',
            name='template_title',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
