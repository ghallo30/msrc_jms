# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20161114_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlefile',
            name='state',
            field=models.CharField(null=True, max_length=4, choices=[('EDIT', 'editor_version'), ('AUTH', 'author_version'), ('REV', 'review_version')]),
        ),
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.CharField(null=True, max_length=4, choices=[('ACK', 'Submission Acknowledge'), ('ACC', 'Accepted Submission'), ('REV', 'Review State'), ('VIS', 'Revision State'), ('RES', 'Resubmit State'), ('DEC', 'Declined Submission'), ('ED', 'Editing State'), ('PUB', 'Published'), ('UPUB', 'Unpublished'), ('WITH', 'Withdrawn Submission')]),
        ),
    ]
