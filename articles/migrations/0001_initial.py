# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('subtitle', models.CharField(max_length=300, null=True)),
                ('cover_letter', models.CharField(max_length=500, null=True)),
                ('references', models.CharField(max_length=500, null=True)),
                ('keywords', models.CharField(max_length=200, null=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('article_version', models.CharField(max_length=300, null=True)),
                ('is_accepted', models.BooleanField(default=False)),
                ('published_by_others', models.BooleanField(default=False)),
                ('is_submitted', models.BooleanField(default=False)),
                ('abstract', models.TextField(null=True)),
                ('likes', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('require_review', models.BooleanField(default=True)),
                ('restrict_access_article', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(null=True)),
                ('issue', models.CharField(max_length=100, null=True)),
                ('volume_number', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=4, choices=[('Accepted Submission', 'ACC'), ('Revisions Required', 'REV'), ('Decline Submission', 'REJ')], null=True)),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='ArticleAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('main_author', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'article_author',
            },
        ),
        migrations.CreateModel(
            name='ArticleFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file_name', models.CharField(max_length=100, null=True)),
                ('file_path', models.FileField(upload_to='article_file')),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'article_file',
            },
        ),
        migrations.CreateModel(
            name='ArticleSubmissionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date_done', models.DateTimeField(auto_now_add=True)),
                ('work_desc', models.CharField(max_length=100)),
                ('att_obj', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cat_name', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Copyright',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('cr_name', models.CharField(max_length=100, null=True)),
                ('cr_description', models.CharField(max_length=300, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'copyright',
            },
        ),
    ]
