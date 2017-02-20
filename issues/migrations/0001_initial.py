# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('issue_volume', models.IntegerField(default=1)),
                ('issue_number', models.IntegerField(default=1)),
                ('issue_year', models.CharField(null=True, max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_submission_expiry', models.DateTimeField(verbose_name='date submission expiry', null=True)),
                ('date_published', models.DateTimeField(verbose_name='date issue published', null=True)),
                ('title', models.CharField(null=True, max_length=300)),
                ('description', models.TextField(null=True)),
                ('date_modified', models.DateTimeField(verbose_name='date issue modified', null=True)),
                ('cover_photo', models.FileField(null=True, upload_to='issue_cover')),
                ('cover_photo_desc', models.TextField(null=True, max_length=300)),
                ('is_published', models.BooleanField(default=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_decline', models.BooleanField(default=False)),
                ('onlineIssn', models.CharField(null=True, max_length=50)),
                ('printIssn', models.CharField(null=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='IssueEditorialBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('publish_email', models.BooleanField(default=True)),
                ('is_displayed', models.BooleanField(default=True)),
                ('issue', models.ForeignKey(null=True, to='issues.Issue')),
            ],
        ),
        migrations.CreateModel(
            name='IssueGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(null=True, max_length=250)),
                ('date_created', models.DateTimeField(verbose_name='date issue created', null=True)),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='issueeditorialboard',
            name='issue_group',
            field=models.ForeignKey(null=True, to='issues.IssueGroup'),
        ),
        migrations.AddField(
            model_name='issueeditorialboard',
            name='issue_member',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
