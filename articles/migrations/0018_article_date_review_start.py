# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0017_auto_20161226_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='date_review_start',
            field=models.DateTimeField(null=True),
        ),
    ]
