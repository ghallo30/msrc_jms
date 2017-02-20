# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jmsmessage',
            name='invitation_accepted',
        ),
        migrations.RemoveField(
            model_name='jmsmessage',
            name='invitation_declined',
        ),
        migrations.AddField(
            model_name='jmsmessage',
            name='date_sent',
            field=models.DateTimeField(verbose_name='date sent', null=True),
        ),
        migrations.AddField(
            model_name='jmsmessage',
            name='date_update',
            field=models.DateTimeField(verbose_name='date updated', null=True),
        ),
    ]
