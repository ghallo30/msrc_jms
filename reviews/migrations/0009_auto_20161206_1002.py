# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0008_reviewdetails_is_invited'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewerElement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('form_text', models.CharField(max_length=250, null=True)),
                ('form_value', models.CharField(max_length=250, null=True)),
                ('form_type', models.CharField(choices=[('T', 'text'), ('S', 'select'), ('C', 'check'), ('R', 'radio')], default='T', max_length=4)),
                ('form_name', models.CharField(max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewerResponse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('response_value', models.CharField(max_length=250, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('is_required', models.BooleanField(default=True)),
                ('order_seq', models.IntegerField(default=1)),
                ('review_element', models.ForeignKey(to='reviews.ReviewerElement', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('form_title', models.CharField(max_length=250, null=True)),
                ('form_description', models.TextField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='reviewerform',
            name='creator',
        ),
        migrations.AddField(
            model_name='assigneditor',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='assigneditor',
            name='is_declined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='max_num_upload',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ReviewerForm',
        ),
        migrations.AddField(
            model_name='reviewerresponse',
            name='review_form',
            field=models.ForeignKey(to='reviews.ReviewForm', null=True),
        ),
        migrations.AddField(
            model_name='reviewdetails',
            name='review_form',
            field=models.ForeignKey(to='reviews.ReviewForm', null=True),
        ),
    ]
