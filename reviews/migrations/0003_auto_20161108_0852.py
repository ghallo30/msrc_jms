# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20161105_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editordecision',
            name='decision',
            field=models.CharField(max_length=4, choices=[('Accepted Submission', 'ACC'), ('Revisions Required', 'REV'), ('Decline Submission', 'REJ')]),
        ),
        migrations.AlterField(
            model_name='editordecision',
            name='stage',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
