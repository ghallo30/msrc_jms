# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0006_policies_content_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Issue',
        ),
        migrations.AlterField(
            model_name='announcement',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='aim',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='cheif_editor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='date_modified',
            field=models.DateTimeField(null=True, verbose_name='journal date modified'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='journal date published'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='start_date',
            field=models.DateTimeField(null=True, verbose_name='journal start date'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
