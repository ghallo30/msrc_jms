# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20161111_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date_submitted',
            field=models.DateTimeField(verbose_name='date submitted', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.CharField(choices=[('Accepted Submission', 'ACC'), ('Review State', 'REV'), ('Revision State', 'VIS'), ('Resubmit State', 'RES'), ('Decline Submission', 'DEC'), ('Editing State', 'ED'), ('Published', 'PUB'), ('Withdrawn Submission', 'WITH')], max_length=4, null=True),
        ),
    ]
