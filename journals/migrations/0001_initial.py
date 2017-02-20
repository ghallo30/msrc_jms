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
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('target_user', models.CharField(max_length=10, choices=[('ALL', 'ALL'), ('AUTH', 'Author'), ('EDIT', 'Editor'), ('REV', 'Reviewer')])),
                ('title', models.CharField(max_length=600)),
                ('content', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_expiry', models.DateTimeField(verbose_name='date expiry')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jms_announcement',
            },
        ),
        migrations.CreateModel(
            name='JMSMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.TextField(null=True)),
                ('title', models.CharField(max_length=500)),
                ('is_opened', models.BooleanField(default=False)),
                ('invitation_accepted', models.BooleanField(default=False)),
                ('invitation_declined', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='actor')),
                ('target', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='target')),
            ],
            options={
                'db_table': 'jms_message',
            },
        ),
        migrations.CreateModel(
            name='JMSTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('content', models.TextField(null=True)),
                ('title', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'db_table': 'jms_template',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('issue', models.CharField(max_length=50)),
                ('aim', models.CharField(max_length=300)),
                ('scope', models.CharField(max_length=320)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('allow_external_submission', models.BooleanField(default=True)),
                ('restrict_access_article', models.BooleanField(default=False)),
                ('require_review', models.BooleanField(default=True)),
                ('journal_rate', models.BooleanField(default=True)),
                ('rate', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('cheif_editor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
