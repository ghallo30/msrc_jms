# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20161105_1201'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('comments_for_editor', models.CharField(null=True, max_length=20)),
                ('comments_for_author', models.CharField(null=True, max_length=120)),
                ('recommendation', models.TextField(null=True)),
                ('date_start', models.DateTimeField(verbose_name='date started')),
                ('date_ended', models.DateTimeField(verbose_name='date ended')),
                ('date_submitted', models.DateTimeField(verbose_name='date_review_submit')),
                ('review_rounds', models.IntegerField(default=0)),
                ('review_files', models.FileField(upload_to='reviewer_files')),
                ('article', models.ForeignKey(null=True, to='articles.Article')),
                ('reviewer', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
