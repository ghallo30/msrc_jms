# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0012_articlekeywords'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('sec_name', models.CharField(null=True, max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'section',
            },
        ),
        migrations.CreateModel(
            name='Submission_Type',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('type_name', models.CharField(null=True, max_length=200)),
                ('type_abbrev', models.CharField(null=True, max_length=200)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='keywords',
        ),
        migrations.AddField(
            model_name='article',
            name='parent_submission',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='articlefile',
            name='is_temp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='articlefile',
            name='review_accessible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='articlefile',
            name='stage',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='articlefile',
            name='state',
            field=models.CharField(null=True, max_length=4, choices=[('EDIT', 'editor_version'), ('AUTH', 'author_version'), ('REV', 'review_version'), ('SUP', 'supp_file')]),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AddField(
            model_name='article',
            name='section',
            field=models.ForeignKey(null=True, to='articles.Section'),
        ),
        migrations.AddField(
            model_name='article',
            name='submission_type',
            field=models.ForeignKey(null=True, to='articles.Submission_Type'),
        ),
    ]
