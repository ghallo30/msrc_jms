# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20161206_1002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editordecision',
            name='review',
        ),
        migrations.RemoveField(
            model_name='editordecision',
            name='stage',
        ),
        migrations.AddField(
            model_name='editordecision',
            name='decided',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelTable(
            name='reviewdetails',
            table='review_details',
        ),
        migrations.AlterModelTable(
            name='reviewerelement',
            table='reviewer_element',
        ),
        migrations.AlterModelTable(
            name='reviewerresponse',
            table='reviewer_response',
        ),
        migrations.AlterModelTable(
            name='reviewform',
            table='review_form',
        ),
    ]
