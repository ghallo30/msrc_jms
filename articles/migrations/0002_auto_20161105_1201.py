# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0001_initial'),
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='copyright',
            name='created_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='created_by'),
        ),
        migrations.AddField(
            model_name='copyright',
            name='modified_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='modified_by'),
        ),
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='articlesubmissionlog',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='articlefile',
            name='article',
            field=models.ForeignKey(to='articles.Article', null=True),
        ),
        migrations.AddField(
            model_name='articlefile',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='article',
            field=models.ForeignKey(to='articles.Article', null=True),
        ),
        migrations.AddField(
            model_name='articleauthor',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='articles.Category'),
        ),
        migrations.AddField(
            model_name='article',
            name='copyright',
            field=models.ForeignKey(to='articles.Copyright', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='journal',
            field=models.ForeignKey(to='journals.Journal', null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='submitting_author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
