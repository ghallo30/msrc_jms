# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20161105_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.CharField(choices=[('Accepted Submission', 'ACC'), ('Revisions Required', 'REV'), ('Decline Submission', 'REJ'), ('Editing State', 'ED'), ('Published', 'PUB'), ('Withdrawn Submission', 'WITH')], max_length=4, null=True),
        ),
    ]
