# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20161108_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='editordecision',
            name='notes_for_author',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='editordecision',
            name='notes_for_editor',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='editordecision',
            name='review',
            field=models.ForeignKey(null=True, to='reviews.ReviewDetails'),
        ),
        migrations.AlterField(
            model_name='editordecision',
            name='decision',
            field=models.CharField(null=True, max_length=4, choices=[('Accepted Submission', 'ACC'), ('Revisions Required', 'REV'), ('Decline Submission', 'REJ'), ('Published', 'PUB'), ('Unpublished', 'UPUB')]),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='date_submitted',
            field=models.DateTimeField(null=True, verbose_name='date review submit'),
        ),
    ]
