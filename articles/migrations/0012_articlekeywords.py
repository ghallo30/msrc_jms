# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_keyword_userinterest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0011_auto_20161206_0847'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('article', models.ForeignKey(to='articles.Article', null=True)),
                ('keyword', models.ForeignKey(to='employee.Keyword', null=True)),
            ],
        ),
    ]
