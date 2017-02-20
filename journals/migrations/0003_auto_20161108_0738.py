# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0002_auto_20161105_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='jmstemplate',
            name='date_modified',
            field=models.DateTimeField(verbose_name='date modified', null=True),
        ),
        migrations.AddField(
            model_name='jmstemplate',
            name='temp_type',
            field=models.CharField(choices=[('EMAIL', 'E'), ('NOTIFICATION', 'N')], null=True, max_length=2),
        ),
    ]
