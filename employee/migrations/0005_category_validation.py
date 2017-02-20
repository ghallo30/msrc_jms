# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_keyword_userinterest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=9)),
                ('is_used', models.BooleanField(default=False)),
                ('expiry_date', models.DateField(null=True, verbose_name='validation expiry date')),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
