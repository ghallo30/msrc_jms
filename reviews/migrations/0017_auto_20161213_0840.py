# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_auto_20161212_0045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewdetails',
            name='review_form',
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='abstract_review',
            field=models.CharField(max_length=2, null=True, choices=[('A', 'Adequate and Relevant'), ('I', 'Inadequate and/or Irrelevant')]),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='abstract_suggestions',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='clarity',
            field=models.CharField(max_length=2, null=True, choices=[('E', 'Excellent'), ('G', 'Good'), ('F', 'Fair'), ('P', 'Poor')]),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='quality',
            field=models.CharField(max_length=2, null=True, choices=[('E', 'Excellent'), ('G', 'Good'), ('F', 'Fair'), ('P', 'Poor')]),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='acceptability',
            field=models.CharField(max_length=2, null=True, choices=[('Y', 'Yes'), ('N', 'No'), ('P', 'Partly')]),
        ),
    ]
