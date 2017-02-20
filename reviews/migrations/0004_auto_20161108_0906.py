# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20161108_0906'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0003_auto_20161108_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignEditor',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date_assigned', models.DateTimeField(auto_now_add=True)),
                ('can_edit', models.BooleanField(default=True)),
                ('can_review', models.BooleanField(default=True)),
                ('date_notified', models.DateTimeField(null=True, verbose_name='Date notified')),
                ('article', models.ForeignKey(to='articles.Article', null=True)),
                ('assigned_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='eic', null=True)),
                ('assoc_editor', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='assoc_edit', null=True)),
            ],
            options={
                'db_table': 'assign_editor',
            },
        ),
        migrations.AlterField(
            model_name='editordecision',
            name='decision',
            field=models.CharField(choices=[('Accepted Submission', 'ACC'), ('Revisions Required', 'REV'), ('Decline Submission', 'REJ')], max_length=4, null=True),
        ),
    ]
