# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_auto_20161213_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewdetails',
            name='comments_for_author',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='reviewdetails',
            name='comments_for_editor',
            field=models.TextField(null=True),
        ),
    ]
