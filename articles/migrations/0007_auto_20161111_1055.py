# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20161110_0032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.CharField(choices=[('Accepted Submission', 'ACC'), ('Review State', 'REV'), ('Decline Submission', 'REJ'), ('Editing State', 'ED'), ('Published', 'PUB'), ('Withdrawn Submission', 'WITH')], null=True, max_length=4),
        ),
    ]
