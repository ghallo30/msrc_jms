# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0016_auto_20161222_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.CharField(choices=[('DRT', 'Draft Submission'), ('ACC', 'Accepted Submission'), ('REV', 'Review State'), ('VIS', 'Revision State'), ('RES', 'Resubmit State'), ('DEC', 'Declined Submission'), ('ED', 'Editing State'), ('PUB', 'Published'), ('UPUB', 'Unpublished'), ('WITH', 'Withdrawn Submission')], null=True, max_length=4),
        ),
    ]
