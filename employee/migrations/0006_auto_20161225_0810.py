# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_category_validation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validation',
            name='created_by',
        ),
        migrations.AddField(
            model_name='validation',
            name='generated_by',
            field=models.ForeignKey(null=True, related_name='generated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='validation',
            name='used_by',
            field=models.ForeignKey(null=True, related_name='used_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
