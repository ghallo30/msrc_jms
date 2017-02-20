# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0013_auto_20161211_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlefile',
            old_name='open_access',
            new_name='main',
        ),
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.CharField(max_length=4, choices=[('ACC', 'Accepted Submission'), ('REV', 'Review State'), ('VIS', 'Revision State'), ('RES', 'Resubmit State'), ('DEC', 'Declined Submission'), ('ED', 'Editing State'), ('PUB', 'Published'), ('UPUB', 'Unpublished'), ('WITH', 'Withdrawn Submission')], null=True),
        ),
    ]
