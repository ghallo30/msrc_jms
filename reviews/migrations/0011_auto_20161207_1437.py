# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20161207_0911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewdetails',
            name='familiarity',
        ),
        migrations.RemoveField(
            model_name='reviewdetails',
            name='max_num_upload',
        ),
        migrations.AddField(
            model_name='editordecision',
            name='is_rescind_descision',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='editordecision',
            name='rescind_descision_date',
            field=models.DateTimeField(null=True, verbose_name='recall date'),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='can_upload',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='is_rescind_descision',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='rescind_descision_date',
            field=models.DateTimeField(null=True, verbose_name='rescind review daate'),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='review_revision',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='recommendation',
            field=models.CharField(max_length=2, choices=[('A', 'Accept Submission'), ('RV', 'Revision Required'), ('D', 'Reject Submission')], null=True),
        ),
    ]
