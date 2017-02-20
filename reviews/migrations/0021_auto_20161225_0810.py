# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0020_assigneditor_is_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewdetails',
            name='assigned_by',
            field=models.ForeignKey(related_name='assigned_by', null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
