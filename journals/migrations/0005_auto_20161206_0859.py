# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0004_jmstemplate_template_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('volume', models.CharField(max_length=10)),
                ('number', models.CharField(max_length=10)),
                ('content', models.TextField(null=True)),
                ('year', models.CharField(null=True, max_length=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_submission_expiry', models.DateTimeField(verbose_name='date submission expiry')),
                ('date_published', models.DateTimeField(null=True, verbose_name='date issue published')),
                ('access_status', models.CharField(null=True, max_length=70)),
                ('title', models.CharField(null=True, max_length=500)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Policies',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(null=True, max_length=10)),
                ('description', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True)),
                ('intended_for', models.CharField(null=True, max_length=70)),
            ],
        ),
        migrations.RemoveField(
            model_name='journal',
            name='issue',
        ),
    ]
